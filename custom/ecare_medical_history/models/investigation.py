from odoo import models, api, fields


class EcMedicalInvestigation(models.Model):
    _name = "ec.medical.investigation"
    _description = "Medical Investigations"
    _order = 'name asc'

    name = fields.Char('Name', required=True)
