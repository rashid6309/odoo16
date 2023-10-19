from odoo import models, fields


class PatientProcedures(models.Model):
    _name = 'ec.patient.procedures'
    _description = 'Patient (Common) Procedures'

    female_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete='restrict')
    male_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete="restrict")

    details = fields.Char('Details')
    date_on = fields.Date('Date On')
