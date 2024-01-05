from odoo import models, api, fields


class EcMedicalYear(models.Model):
    _name = "ec.medical.year"
    _description = "Year"
    _order = 'year desc'
    _rec_name = "year"

    year = fields.Integer('Year', required=True)
