from odoo import models, fields


class FemaleLabHistory(models.Model):
    _name = 'ec.female.lab.history'
    _description = "Lab History"

    first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation")

    name = fields.Char(string="Name")
    date = fields.Date(sting="Date")

    attachment_id = fields.Many2one(comodel_name="ir.attachment")

