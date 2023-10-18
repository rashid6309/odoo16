from odoo import models, api, fields


class EcMedicalInvestigation(models.Model):
    _name = "ec.medical.investigation"
    _description = "Medical Investigations"
    _order = 'create_date desc'

    name = fields.Char('Name', required=True)
