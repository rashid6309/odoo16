import logging
from odoo import api, fields, models, _


class MedicalDiagnosis(models.Model):
    _name = 'ec.medical.diagnosis'
    _description = 'Medical Diagnosis'

    name = fields.Char("Name", required=True)
