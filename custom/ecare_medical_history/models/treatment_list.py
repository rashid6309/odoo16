from odoo import models, fields


class TreatmentList(models.Model):
    _name = "ec.medical.treatment.list"
    _description = "Medical Treatment List"
    _order = 'name asc'

    name = fields.Char(required=True,)
