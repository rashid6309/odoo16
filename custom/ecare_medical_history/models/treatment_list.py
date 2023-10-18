from odoo import models, fields


class TreatmentList(models.Model):
    _name = "ec.medical.treatment.list"
    _description = "Medical Treatment List"
    _order = 'create_date desc'

    name = fields.Char(required=True,)
