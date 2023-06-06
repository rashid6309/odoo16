from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.exceptions import AccessError

import datetime
import math


class EcareAppointmentSlot(models.Model):
    _name = "ec.booked.slot.record"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Appointment for the partner"
    _rec_name = "partner_id"

    state = fields.Selection(selection=[('Booked', "Booked"),
                                        ('Cancelled', "Cancelled"),
                                        ('Blocked', "Blocked"),
                                        ('Rescheduled Required', "Rescheduled Required"),
                                        ],
                             string="State",
                             default='Booked',
                             tracking=True,
                             )

    partner_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 tracking=True,
                                 ondelete="restrict",
                                 string="Patient")

    partner_selection_choices = fields.Selection(selection=[('existing', 'Existing'),
                                                           ('new', 'New')],
                                               string="Patient Selection",
                                               default='existing')

    existing_partner_id = fields.Many2one(comodel_name="ec.medical.patient",
                                          tracking=True,
                                          store=False,
                                          string="Existing Patient",
                                         )

    new_partner_id = fields.Many2one(comodel_name="ec.medical.patient",
                                     tracking=False,
                                     string="New Patient",
                                     store=False)

    category = fields.Many2one(comodel_name="ec.slot.category",
                               tracking=True,
                               ondelete='restrict',
                               string='Category')

    ''' It is required in the FE for the JS to render relevant dashboard '''
    category_id = fields.Char(string='Category Id',
                              compute='_compute_category_id', )

    sub_category = fields.Many2one(comodel_name="ec.slot.sub.category",
                                   tracking=True,
                                   ondelete='restrict',
                                   string='Sub-Category')

    date = fields.Date('Date',
                       required=True,
                       tracking=True,
                       default=lambda self: datetime.date.today())

    start = fields.Char(string='Start Time',
                        required=True,
                        tracking=True,)

    stop = fields.Char(string='End Time',
                       required=True,
                       tracking=True,
                       readonly=False,
                       store=True,)

    consultant_id = fields.Many2one(comodel_name="res.consultant",
                                    string="Staff",
                                    ondelete='restrict',
                                    required=False)

    configurator = fields.Many2one(comodel_name="ec.slot.configurator",
                                   tracking=True,
                                   string="Configurator",
                                   ondelete='restrict',
                                   store=True)

    block_sms = fields.Boolean(string="Block SMS",
                               tracking=True,
                               default=False)

    partner_checked = fields.Boolean('Checked',
                                     tracking=True,
                                     default=True, )

    comment = fields.Text(string="Comment")

    # it is being used in product_id domain side (Removed fully at xml)
    # Now it is also commented on the ec.slot.category
    # product_ids = fields.Many2many(related="category.product_ids")

    product_id = fields.Many2one(comodel_name="product.product",
                                 ondelete='restrict')

    # Used to be store in patient --> Preferred Mobile No.
    mobile_no = fields.Char(string='Preferred Mobile No.',
                            tracking=True)

    ''' XXX - Linked to mobile no and patient preferred no  - XXX'''
    # If the number added here it'll be updated at the patient
    # If the patient number is updated it'll also reflect back at here
    @api.onchange("partner_id")
    def onchange_partner(self):
        for obj in self:
            if obj.partner_id and obj.partner_id.preferred_mobile:
                obj.mobile_no = obj.partner_id.preferred_mobile
            else:
                obj.mobile_no = None

    @api.onchange('partner_selection_choices')
    def onchange_partner_selection_choices(self):
        self.partner_id = None
        self.existing_partner_id = None
        self.new_partner_id = None
        self.onchange_partner()

    @api.onchange('existing_partner_id')
    def onchange_existing_partner(self):
        self.partner_id = self.existing_partner_id.id
        self.onchange_partner()

    @api.onchange('new_partner_id')
    def onchange_new_partner(self):
        self.partner_id = self.new_partner_id
        self.onchange_partner()

    @api.onchange("mobile_no")
    def onchange_mobile_no(self):
        for obj in self:
            if partner_id := obj.partner_id:
                # Admin action
                partner_id.sudo().write({
                    'preferred_mobile' : obj.mobile_no
                })

    ''' XXX - ENd here - XXX '''


    @api.constrains('state', 'category', 'sub_category', 'date', 'start', 'stop')
    def _check_unique_slot(self):
        for record in self:
            if record.state == 'Booked':
                self.env.cr.execute(
                    'SELECT id FROM ec_booked_slot_record WHERE category = %s AND sub_category = %s AND date = %s AND '
                    'start = %s AND stop = %s AND state = %s',
                    (record.category.id, record.sub_category.id, record.date, record.start, record.stop, record.state)
                )
                rec = self.env.cr.fetchone()
                if self.env.cr.fetchone():
                    raise AccessError("Slot is booked.")

    @api.constrains('category', 'partner_id')
    def _check_unique_primary_category(self):
        """
        *** It will check that one patient/partner can have only one appointment in the same primary category.
        :return:
        """
        if not self.partner_id: # in case of block
            return

        query = """  select
            count(1)
        from
            ec_booked_slot_record ebsr
        inner join ec_slot_category esc on
            esc.id = ebsr.category
        inner join ec_slot_category esc2 on
            esc.parent_category_id = esc2.id
        where
            ebsr.state = 'Booked' -- State
            and date = '{}' -- Date
            and ebsr.partner_id  = {} -- Patient
            and esc2.id = {} -- Parent/Primary Category
            and esc.id = {}; -- Secondary Category
        """.format(self.date,
                   self.partner_id.id, # Patient/Partner
                   self.category.parent_category_id.id, # Parent/Primary Category
                   self.category.id
                   ) # Secondary Category

        self._cr.execute(query)
        result = self._cr.fetchone()
        if result[0] > 1:
            raise AccessError("Only One appointment is allowed in a day.")

        return True

    def action_rescheduled_slot(self):
        self.ensure_one()
        # update_self = self.env['ec.slot.category'].get_slots_record_category_day_data(str(self.date), self.category.id)
        action = self.env['ir.actions.client']._for_xml_id("ecare_appointment.ec_appointment_action_dashboard")
        return action

    @api.constrains('start_dt', 'end_dt')
    def check_start_end_dt(self):
        self.ensure_one()
        if self.end_dt <= self.start_dt:
            raise UserError("End time can't be less then start time.")

    def search_slots(self, start, end, date, cat, sub_cat):
        """
        # Improvement: It should fetch all the appointments of the day and then search_slot should search from that.

        It will search the one appointment with the "Booked" and "Blocked" status.
        :param start: Start time (Day time without date)
        :param end: End time (Day time without date)
        :param date: Date
        :param cat: Secondary Category
        :param sub_cat: Sub Category

        :return: Matching records
        """
        record = self.search(domain=[('start', '=', start),
                                     ('stop', '=', end),
                                     ('date', '=', date),
                                     ('category', '=', cat),
                                     ('sub_category', '=', sub_cat),
                                     ('state', 'in', ['Booked', 'Blocked'])],
                             limit=1)

        return record

        # self._cr.execute("select * from ec_appointment_slot_record isr where date = '2022-11-28' and category = 1 and "
        #                  "sub_category = 1 and start = '1000'and stop = '1030'")

        # @api.model

    @api.model
    def cancel_booking(self, booking_id):
        record = self.env['ec.booked.slot.record'].browse(int(booking_id))
        if record:
            record.state = 'Cancelled'
        return record

    @api.model
    def switch_slot_record(self, existing_slot_id, start, end, date, cat, sub_cat, configurator_id):
        record = self.env['ec.booked.slot.record'].search([
            ('start', '=', start),
            ('stop', '=', end),
            ('date', '=', date),
            ('category', '=', cat),
            ('sub_category', '=', sub_cat),
            ('state', '=', 'Booked'),
        ], limit=1)
        if record:
            return {

                'warning': {

                    'title': 'Warning!',

                    'message': 'There is some error, contact your admin.'}

            }
        slot = self.env['ec.booked.slot.record'].browse(existing_slot_id)
        # appointment_id = self.env['ec.booked.slot.record'].browse(appointment_id)
        if slot:
            return slot.write(
                {
                    'start': start,
                    'stop': end,
                    'date': date,
                    'category': cat,
                    'sub_category': sub_cat,
                    'state': 'Booked',
                    'configurator': configurator_id,
                }
            )
        else:
            return {

                'warning': {

                    'title': 'Warning!',

                    'message': 'There is some error, contact your admin.'}

            }

    @api.model
    def _compute_category_id(self):
        if self.category:
            self.category_id = self.category.id

    @api.model
    def get_block_slot_form_view_id(self):
        """
        The view with id must exist
        xml id: block_slot_form_view
        :return:
        """
        return self.env.ref('ecare_appointment.block_slot_form_view').id or None

    def execute_query(self):
        # Get the total number of records
        limit = 2
        offset = 2
        total_query = """
                    SELECT COUNT(*)
                    FROM
                account_payment payment
            JOIN account_move move ON
                move.id = payment.move_id
            JOIN account_move_line line ON
                line.move_id = move.id	
            JOIN account_partial_reconcile part ON
                part.debit_move_id = line.id
                OR
                    part.credit_move_id = line.id
            JOIN account_move_line counterpart_line ON
                part.debit_move_id = counterpart_line.id
                OR
                    part.credit_move_id = counterpart_line.id
            JOIN account_move invoice ON
                invoice.id = counterpart_line.move_id
            join account_move_line invoice_line on
            invoice.id = invoice_line.move_id
            join product_product pp
            on invoice_line.product_id   = pp.id
            join product_template pt
            on pp.product_tmpl_id  = pt.id
            JOIN account_account account ON
                account.id = line.account_id
            join account_journal aj
            on aj.id = line.journal_id
            join res_partner rp
            on line.partner_id = rp.id
            WHERE
                account.account_type IN ('asset_receivable', 'liability_payable')
                AND 
                line.id != counterpart_line.id
                AND invoice.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                GROUP BY payment.create_date,move."name", rp.display_name, 
                part.amount , move.state,invoice.name,aj.name,invoice.amount_total 
        """
        self._cr.execute(total_query)
        total_records = self._cr.fetchone()[0]

        # Calculate total pages
        total_pages = math.ceil(total_records / limit)

        # Get the records with pagination
        query = """
            SELECT json_build_object(
                'header', (SELECT json_build_array(
                    'Date',
                    'Patient',
                    'Payment Ref',
                    'Services',
                    'INV #',
                    'Mode',
                    'INV Amount',
                    'Settled Amount'
                ) FROM account_move LIMIT 1),
                'data', json_build_array(
                    payment.create_date,
                    rp.display_name,
                    move.name,
                    string_agg(pt."name"->>'en_US', ','),
                    invoice.name, 
                    aj."name",
                    invoice.amount_total,
                    part.amount,
                    move.state
                )
            ) AS result
            FROM
                account_payment payment
            JOIN account_move move ON
                move.id = payment.move_id
            JOIN account_move_line line ON
                line.move_id = move.id	
            JOIN account_partial_reconcile part ON
                part.debit_move_id = line.id
                OR
                    part.credit_move_id = line.id
            JOIN account_move_line counterpart_line ON
                part.debit_move_id = counterpart_line.id
                OR
                    part.credit_move_id = counterpart_line.id
            JOIN account_move invoice ON
                invoice.id = counterpart_line.move_id
            join account_move_line invoice_line on
            invoice.id = invoice_line.move_id
            join product_product pp
            on invoice_line.product_id   = pp.id
            join product_template pt
            on pp.product_tmpl_id  = pt.id
            JOIN account_account account ON
                account.id = line.account_id
            join account_journal aj
            on aj.id = line.journal_id
            join res_partner rp
            on line.partner_id = rp.id
            WHERE
                account.account_type IN ('asset_receivable', 'liability_payable')
                AND 
                line.id != counterpart_line.id
                AND invoice.move_type IN ('out_invoice', 'out_refund', 'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                GROUP BY payment.create_date,move."name", rp.display_name, 
                part.amount , move.state,invoice.name,aj.name,invoice.amount_total 	
                LIMIT {} OFFSET {}
        """.format(limit, offset)
        self._cr.execute(query)
        records = self._cr.fetchall()

        header = [record[0]['header'] for record in records]
        data = [record[0]['data'] for record in records]

        result = {
            'header': header,
            'data': data,
            'total_records': total_records,
            'total_pages': total_pages
        }
        return result

