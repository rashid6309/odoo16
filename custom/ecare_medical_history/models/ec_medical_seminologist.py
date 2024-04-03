import logging
from odoo import api, fields, models, _


class MedicalSeminologist(models.Model):
    _name = 'ec.medical.seminologist'
    _description = 'Medical Seminologist'
    _order = 'name asc'

    name = fields.Char("Name", required=True)
    user_id = fields.Many2one(comodel_name='res.users', string='Related User')
