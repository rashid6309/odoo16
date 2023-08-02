from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ecare_invoicing.models.product_template import ProductTemplate


class AccountMove(models.Model):
    _inherit = 'account.move'
    _order = "id desc"

    invoice_date = fields.Date(
        string='Invoice/Bill Date',
        readonly=True,
        default=lambda self: fields.datetime.now(),
        states={'draft': [('readonly', False)]},
        index=True,
        copy=False,
    )

    move_type = fields.Selection(
        selection=[
            ('entry', 'Journal Entry'),
            ('out_invoice', 'Customer Invoice'),
            ('out_refund', 'Customer Refund Note'),
            ('in_invoice', 'Vendor Bill'),
            ('in_refund', 'Vendor Credit Note'),
            ('out_receipt', 'Sales Receipt'),
            ('in_receipt', 'Purchase Receipt'),
        ],
        string='Type',
        required=True,
        readonly=True,
        tracking=True,
        change_default=True,
        index=True,
        default="entry",
    )

    sub_category_id = fields.Many2one(comodel_name='ec.slot.sub.category',
                                      string="Location",
                                      )

    ''' For showing purpose only '''
    # this compute will compute below
    total_receivable = fields.Monetary(string="Invoiced",
                                   compute="_calculate_invoice_stats",
                                   readonly=True,
                                  )

    payment_amount = fields.Monetary(string="Net amount",
                                     readonly=True,
                                     compute="_calculate_invoice_stats",
                                     store=False)

    # Dependant upon "payment_amount" due to compute method being triggered in there.
    refund_amount = fields.Monetary(string="Refund",
                                    compute="_calculate_invoice_stats",
                                    readonly=True,
                                    store=False)

    discount_amount = fields.Monetary(string="Discount",
                                      compute="_calculate_invoice_stats",
                                      readonly=True,
                                      store=False)


    ''' Override Methods '''

    @api.model_create_multi
    def create(self, vals):
        obj = super(AccountMove, self).create(vals)
        obj.handle_section()
        obj.handle_pharmacy_lines()
        obj.product_price_unit_refund()
        if obj.partner_id:
            patient_id = obj.get_patient_against_partner()
            patient_id.update_write_date()

        return obj

    def write(self, vals):
        """
        DON'T Repeat check is critical else it'll be in recursive.
        """
        dont_repeat = False
        if vals.get('dont_repeat'):
            dont_repeat = vals.pop('dont_repeat')

        obj =  super(AccountMove, self).write(vals)
        if not dont_repeat and vals.get("invoice_line_ids"):
            self.handle_section()

        if vals.get("invoice_line_ids"):
            self.onchange_line_refund()


        if self.partner_id:
            patient_id = self.get_patient_against_partner()
            patient_id.update_write_date()

        return obj

    ''' End here '''

    def get_patient_against_partner(self):
        patient_id = self.env['ec.medical.patient'].search(domain=[('partner_id', '=', self.partner_id.id)])
        return patient_id

    def _calculate_invoice_stats(self):

        for line in self:

            net_amount = 0.0
            total_discount = 0.0
            refund_amount = 0.0

            total_invoice = line.amount_total_signed
            if  line.move_type == 'out_refund' or line.payment_state != 'paid':
                line.write({
                    'payment_amount': net_amount,
                    'discount_amount': total_discount,
                    'refund_amount': refund_amount,
                    'total_receivable': total_invoice,
                })
                continue

            refund_invoices  = self.env['account.move'].search(domain=[('move_type', '=', 'out_refund'),
                                                                       ('payment_state', '=', 'paid'),
                                                                       ('reversed_entry_id', '=', line.id)])
            refund_amount = 0.0
            if refund_invoices:
               refund_amount = sum([invoice.amount_total_signed for invoice in refund_invoices])

            total_discount = -1 * sum([invoice_line.fixed_amount_discount for invoice_line in line.invoice_line_ids])

            net_amount = line.amount_total_signed + refund_amount
            total_invoice += abs(total_discount)

            line.write({
                'payment_amount': net_amount,
                'discount_amount': total_discount,
                'refund_amount': refund_amount,
                'total_receivable': total_invoice,
            })

    def handle_section(self):
        """
        If product added it'll auto sequence the products with by looking its product Type.

        EXCEPTION CASE: If added more than 100 products it'll not work. But it's not possible still incase.

        SEQUENCE: In which Type Selection list is. 0 index --> 100-199, 1 index --> 200-299 and so on.

        DO KNOW:
        All operations here are in bulk so please don't change these to single write/create or delete due to performance.
        :return:
        """
        DEFAULT_SEQUENCE = 100

        vals = []
        move_lines = []
        for index, tuple_data in enumerate(ProductTemplate.TYPE_SELECTION):
            section, _ = tuple_data

            sequence = (index + 1) * DEFAULT_SEQUENCE
            # Filter sections-products
            section_product_lines = self.invoice_line_ids.filtered(lambda x: x.product_id.service_type ==  section)
            # Check if section existed before or not.

            section_line = self.invoice_line_ids.filtered(lambda x: x.display_type == 'line_section'
                                                                    and x.name == section)
            if not section_line and section_product_lines:
                vals.append({
                    'move_id': self.id,
                    'name': section,
                    'display_type': 'line_section',
                    'sequence': sequence,
                })
            elif section_line and not section_product_lines: # If the section line is present but no related products
                move_lines.append((2, section_line.id))
            elif section_line.sequence != sequence: # client action: Sequence changed by user.
                move_lines.append([1, section_line.id, {'sequence': sequence}])

            for line in section_product_lines:
                sequence += 1
                if line.sequence != sequence: # don't add unnecessary lines.
                    move_lines.append([1, line.id, {'sequence': sequence}])

        if move_lines:
            self.write({'invoice_line_ids': move_lines, 'dont_repeat': True})

        if vals:
            self.env['account.move.line'].create(vals)

        return True

    def product_price_unit_refund(self):
        if self.move_type != 'out_refund':
            return

        move_product_lines = self.invoice_line_ids.filtered(lambda x: x.display_type == 'product')
        if not move_product_lines:
            return

        for line in move_product_lines:
            price_unit = line.price_subtotal / line.quantity
            line.price_unit = price_unit
            line.paid_subtotal = line.quantity * price_unit
            line.refund_amount = 0
            line.discount =  100

        self.onchange_line_refund()

    def onchange_line_refund(self):
        if self.move_type != 'out_refund':
            return

        product_invoice_lines = self.invoice_line_ids.filtered(lambda x: x.display_type == 'product' and x.refund_amount > 0.0)
        product_invoice_lines.onchange_refund_amount()

    def action_open_refund_notes(self):
        refund_invoices = self.env['account.move'].search(domain=[('move_type', '=', 'out_refund'),
                                                                  ('reversed_entry_id', '=', self.id)])

        if refund_invoices:
            return {
                "name": _("Refund Notes"),
                "type": 'ir.actions.act_window',
                "res_model": 'account.move',
                'views': [(self.env.ref('account.view_out_credit_note_tree').id, 'tree'),
                          (self.env.ref('ecare_invoicing.refund_view_move_form').id, 'form')
                          ],
                'view_mode': 'tree,form',
                'context': {'default_move_type': 'out_refund'},
                'domain': [('id', 'in', refund_invoices.ids),
                           ('move_type', '=', 'out_refund')],
            }
        raise ValidationError("No refund has been made yet.")

    @api.model
    def find_patient(self):
        patient = self.env['ec.medical.patient'].search([
            ('partner_id', '=', self.partner_id.id),
        ])
        if patient:
            return patient
        else:
            raise UserError("No patient found.")

    def get_mode_of_payment(self):
        """
        Used in Report Mode of payment.
        If multiple payments it'll show those by , seperated
        :return: journal_name
        """
        journal_name = ""

        payment_journals = self.invoice_payments_widget
        if not payment_journals:
            return journal_name

        contents = payment_journals['content']
        for line in contents:
            journal_name_to_add = line.get("journal_name", "")
            if journal_name != "":
                journal_name += ','
            journal_name += journal_name_to_add

        return journal_name

    def handle_pharmacy_lines(self):
        """
        If not administrator exclude the services_types which are listed below.
        :return:
        """
        if self.move_type != 'out_refund':
            return

        if self.env.user.has_group('account.group_account_manager'):
            return

        product_service_types = ['Pharmacy', 'Laboratory', 'Radiology']
        invoice_line_product = self.invoice_line_ids.filtered(lambda x: x.product_id.service_type
                                                                        in product_service_types or
                                                                        x.name in product_service_types)
        invoice_line_product.unlink()

    def button_draft(self):
        """
        Handling line_refund if given.

        Why: Basically when it reset it changed the subtotal to unit_price due to default onchange now handled that.

        :return:
        """
        super(AccountMove, self).button_draft()
        self.onchange_line_refund()

    def action_reverse(self):
        """
        Adding check so that amount shouldn't be greater than the total invoiced amount.
        """

        refund_invoices = self.env['account.move'].search(domain=[('move_type', '=', 'out_refund'),
                                                ('reversed_entry_id', '=', self.id)])

        receivable_against_invoice = self.amount_total_signed # Which
        already_refunded = 0.0

        if refund_invoices:
            already_refunded = sum([invoice.amount_total_signed for invoice in refund_invoices])

        can_be_refund = receivable_against_invoice + already_refunded

        if can_be_refund  == 0:
            raise UserError("Invoice is refunded already.")

        ''' Below is the default behaviour'''
        action = self.env["ir.actions.actions"]._for_xml_id("account.action_view_account_move_reversal")

        if self.is_invoice():
            action['name'] = _('Refund Note')


        return action
