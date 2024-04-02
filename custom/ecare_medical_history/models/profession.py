from odoo import models, api, fields


class EcMedicalProfession(models.Model):
    _name = "ec.medical.profession"
    _description = "Medical Professions"
    _order = 'name asc'

    name = fields.Char('Name', required=True)
