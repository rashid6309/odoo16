from odoo import models, fields


class ConsultationType(models.Model):
    _name = "consultation.type"
    _description = "Consultation Type"

    name = fields.Char(string="Name",
                       required=True)

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'Name must be unique'),
    ]
