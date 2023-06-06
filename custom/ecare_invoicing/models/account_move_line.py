from odoo import models, fields, api
from odoo.exceptions import ValidationError




class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    fixed_amount_discount = fields.Monetary(string="Discount Amount",
                                            default=0.0,
                                            copy=False,
                                            tracking=True)

    refund_amount = fields.Monetary(string="Refund Amount",
                                    default=0.0,
                                    copy=False,
                                    tracking=True)

    service_type = fields.Selection(related='product_id.service_type')

    @api.onchange("price_subtotal", "price_unit", "fixed_amount_discount")
    def onchange_discount_amount(self):
        for line in self:
            if line.move_id.move_type != 'out_invoice':
                return

            if line.fixed_amount_discount <= 0.0:
                line.fixed_amount_discount = 0.0
                line.discount = 0
                return

            price_subtotal = line.quantity * line.price_unit

            if 0.0 < line.fixed_amount_discount <= price_subtotal:
                subtotal = line.quantity * line.price_unit
                line.discount = line.fixed_amount_discount /  subtotal * 100
            else:
                if line.discount != 0.0:
                    line.discount = 0.0

                raise ValidationError("Discount amount should be greater than 0 and less than price")

    @api.onchange("refund_amount")
    def onchange_refund_amount(self):
        for line in self:
            if line.move_id.move_type != 'out_refund':
                return

            if line.refund_amount <= 0.0:
                line.refund_amount = 0.0
                line.discount = 100
                return

            price_subtotal = line.price_unit * line.quantity
            if 0.0 < line.refund_amount <= price_subtotal:
                refund_discount = 100 - (line.refund_amount / price_subtotal) * 100
                line.discount = refund_discount
            else:
                raise ValidationError("Refund amount should be greater than 0 and less than price")


    @api.depends('product_id', 'journal_id')
    def _compute_name(self):
        for line in self:
            if line.display_type == 'payment_term':
                if line.move_id.payment_reference:
                    line.name = line.move_id.payment_reference
                elif not line.name:
                    line.name = ''
                continue
            if not line.product_id or line.display_type in ('line_section', 'line_note'):
                continue
            if line.partner_id.lang:
                product = line.product_id.with_context(lang=line.partner_id.lang)
            else:
                product = line.product_id
            # I'm using the product.name instead of partner_ref
            values = []
            if product.partner_ref:
                values.append(product.name)
            if line.journal_id.type == 'sale':
                if product.description_sale:
                    values.append(product.description_sale)
            elif line.journal_id.type == 'purchase':
                if product.description_purchase:
                    values.append(product.description_purchase)
            line.name = '\n'.join(values)