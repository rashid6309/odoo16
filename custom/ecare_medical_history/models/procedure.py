from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.date_validation import DateValidation

class PatientProcedures(models.Model):
    _name = 'ec.patient.procedures'
    _description = 'Patient (Common) Procedures'

    female_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete='restrict')
    male_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete="restrict")

    details = fields.Char('Details')
    date_on = fields.Date('Date On', required=True)

    @api.onchange('date_on')
    def _check_date_on_date(self):
        if self.date_on:
            return DateValidation._date_validation(self.date_on)
