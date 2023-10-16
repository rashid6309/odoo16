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

    color = fields.Integer('Color Index')

    '''This wizard will be used in case if we need to make that edit button along with factors functional'''


class EcMedicalFactorsWizard(models.TransientModel):
    _name = "ec.medical.factors.wizard"
    _description = "Wizard to select Factors"

    factor_ids = fields.Many2many('ec.medical.factors', required=1)
