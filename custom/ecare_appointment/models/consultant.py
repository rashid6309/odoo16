from odoo import models, fields


class Consultant(models.Model):
    _name = "res.consultant"
    _description = "Staff"

    name = fields.Char(string="Name",
                       required=True)
