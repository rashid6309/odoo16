from odoo import models, fields


class PatientProcedures(models.Model):
    _name = 'ec.medical.patient.procedures'
    _description = 'Patient Procedures'

    first_consultation_id = fields.Many2one('ec.first.consultation')

    details = fields.Char('Details')
    date_on = fields.Date('Date ON')