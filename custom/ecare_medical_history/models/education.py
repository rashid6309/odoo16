from odoo import models, api, fields


class EcMedicalEducation(models.Model):
    _name = "ec.medical.education"
    _description = "Medical Educations"
    _order = 'name asc'

    name = fields.Char('Name', required=True)
