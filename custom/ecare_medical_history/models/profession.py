from odoo import models, api, fields


class EcMedicalProfession(models.Model):
    _name = "ec.medical.profession"
    _description = "Medical Professions"
    _order = 'create_date desc'

    name = fields.Char('Name', required=True)
