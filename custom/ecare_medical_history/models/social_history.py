from odoo import models, fields


class SocialHistory(models.Model):
    _name = "ec.social.history"
    _description = "Social History"

    social_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                ondelete='restrict')

    ''' Female '''
    female_education_id = fields.Many2one(comodel_name="ec.medical.education",
                                          string="Education")
    female_education = fields.Text(string="Other")
    female_profession_id = fields.Many2one(comodel_name="ec.medical.profession",
                                           string="Profession")
    female_profession = fields.Text(string="Other")
    female_dependence = fields.Text(string="Dependence")

    ''' Male '''

    male_education_id = fields.Many2one(comodel_name="ec.medical.education",
                                        string="Education")
    male_education = fields.Text(string="Other")
    male_profession_id = fields.Many2one(comodel_name="ec.medical.profession",
                                         string="Profession")
    male_profession = fields.Text(string="Other")
    male_dependence = fields.Text(string="Dependence")
