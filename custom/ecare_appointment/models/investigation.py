from odoo import models, api, fields


class EcMedicalInvestigation(models.Model):
    _name = "ec.medical.investigation"
    _description = "Investigations"

    name = fields.Char('Name')
