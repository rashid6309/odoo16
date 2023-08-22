from odoo import api, models, fields, _


class FamilyHistory(models.Model):
    _name = 'ec.medical.patient.family.history'
    _description = 'Family History'
    _rec_name = 'name'

    name = fields.Char(string='Family Member')
