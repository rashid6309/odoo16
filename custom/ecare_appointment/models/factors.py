from odoo import models, api, fields


class EcMedicalFactors(models.Model):
    _name = "ec.medical.factors"
    _description = "Medical Factor"
    _order = 'create_date desc'

    type = fields.Selection(string='Type', required=1,
                            selection=[('male', 'Male'),
                                       ('female', 'Female')],
                            )
    name = fields.Char('Name', required=True)
