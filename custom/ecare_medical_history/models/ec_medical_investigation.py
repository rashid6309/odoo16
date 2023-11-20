import logging
from odoo import api, fields, models, _


class MedicalInvestigation(models.Model):
    _name = 'ec.medical.investigation'
    _description = 'Medical Investigation'

    name = fields.Char("Name", required=True)
