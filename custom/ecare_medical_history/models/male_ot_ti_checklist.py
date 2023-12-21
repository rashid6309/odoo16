from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MaleOtTiChecklist(models.Model):
    _name = 'male.ot.ti.checklist'
    _description = 'Male Pre OI/TI Checklist'

    # Male Pre-OI/TI Checklist Fields
    male_semen_analysis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                           string='Semen Analysis within normal limits and up to date?')

    husband_availability_male = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                 string='Husband Availability during cycle?')

    frozen_sample_available_male = fields.Boolean(string='Is frozen sample available and adequate for IUI?')

    risk_inability_to_give_samples_male = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                           string='Risk of inability to give samples (trauma, mental health, medical disease e.g. diabetes)')
