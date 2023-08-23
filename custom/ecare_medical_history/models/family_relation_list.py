from odoo import api, models, fields, _


class FamilyHistoryDiseases(models.Model):
    _name = 'ec.family.relation.list'
    _description = 'Family History Relations'
    _rec_name = 'name'

    name = fields.Char(string='Name')
