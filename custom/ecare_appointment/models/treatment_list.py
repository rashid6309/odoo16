from odoo import models, fields


class TreatmentList(models.Model):
    _name = "ec.medical.treatment.list"

    name = fields.Char()
