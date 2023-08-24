from odoo import models, fields


class PatientProcedures(models.Model):
    _name = 'ec.patient.procedures'
    _description = 'Patient Procedures'

    female_consultation_id = fields.Many2one(comodel_name='ec.first.consultation')
    male_consultation_id = fields.Many2one(comodel_name='ec.first.consultation')

    details = fields.Char('Details')
    date_on = fields.Date('Date ON')
