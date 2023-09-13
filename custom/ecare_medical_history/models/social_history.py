from odoo import models, fields


class SocialHistory(models.Model):
    _name = "ec.social.history"
    _description = "Social History"

    ''' Female '''
    female_education = fields.Text(string="Education")
    female_profession = fields.Text(string="Profession")
    female_dependence = fields.Text(string="Dependence")

    ''' Male '''

    male_education = fields.Text(string="Education")
    male_profession = fields.Text(string="Profession")
    male_dependence = fields.Text(string="Dependence")
