from odoo import api, models, fields, _


class EcMedicalMultiSelection(models.Model):
    _name = 'ec.medical.multi.selection'

    name = fields.Char(string='Name')
    type = fields.Char(string="Type")
