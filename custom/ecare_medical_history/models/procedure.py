from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.validation import Validation


class PatientProcedures(models.Model):
    _name = 'ec.patient.procedures'
    _description = 'Patient (Common) Procedures'
    _order = 'date_on desc'

    female_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete='restrict')
    male_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete="restrict")

    details = fields.Char('Details')
    date_on = fields.Date('Date On', required=True)

    surgical_year_id = fields.Many2one(
        comodel_name="ec.medical.year",
        string='Year',
        help='Select a year from the list',
    )

    @api.onchange('date_on')
    def _check_date_on_date(self):
        if self.date_on:
            return Validation._date_validation(self.date_on)
