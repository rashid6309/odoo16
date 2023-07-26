from odoo import models, fields, _


class PatientInvoiceHistory(models.TransientModel):
    _name = "patient.account.move.line.history"
    _description = "Patient History"
    _order = "datetime desc"

    datetime = fields.Datetime(string="Date")

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 string="Patient")

    move_id = fields.Many2one(comodel_name="account.move",
                              string="Invoice #")

    product_id = fields.Many2one(comodel_name="product.product",
                                 string="Product")

    invoice_type = fields.Char(string="Type")

    payment_state = fields.Char(string="Status")

    amount = fields.Float(string="Subtotal")

    def action_view_record(self):
        view_id = self.env.ref('account.view_move_form').id
        if self.invoice_type == 'Refund':
            view_id = self.env.ref('ecare_invoicing.refund_view_move_form').id

        return{
            "name": _("Invoice"),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_id': view_id,
            'res_model': 'account.move',
            'res_id': self.move_id.id,
            'context': {'default_partner_id': self.patient_id.partner_id.id},
        }

