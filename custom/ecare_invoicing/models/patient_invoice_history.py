from odoo import models, fields


class PatientInvoiceHistory(models.TransientModel):
    _name = "patient.account.move.line.history"
    _description = "Patient History"

    datetime = fields.Datetime(string="Date")

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 string="Patient")

    move_id = fields.Many2one(comodel_name="account.move",
                              string="Invoice #")

    product_id = fields.Many2one(comodel_name="product.product",
                                 string="Service")

    invoice_type = fields.Char(string="Type")

    payment_state = fields.Char(string="Status")

    amount = fields.Float(string="Subtotal")

