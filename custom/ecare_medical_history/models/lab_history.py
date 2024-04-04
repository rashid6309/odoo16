from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.validation import Validation


class LabHistory(models.Model):
    _name = "ec.lab.history"
    _description = "Patient Lab History"
    _order = 'date desc'

    female_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")
    male_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")

    filename = fields.Char(string="Filename")

    attachment_id = fields.Binary(string="Document")

    results = fields.Text('Results', required=True)

    @api.onchange('date')
    def _check_lab_date(self):
        if self.date:
            return Validation._date_validation(self.date)

