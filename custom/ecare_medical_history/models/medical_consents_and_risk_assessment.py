from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class ConsentsRiskAssessment(models.Model):
    _name = 'medical.consents.risk.assessment'
    _description = 'Consents Risk Assessment'

    counselling_multiple_birth = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                  string='Counselled regarding risk of multiple birth?')
    counselling_multiple_birth_decision = fields.Char(string='Counselled regarding risk of multiple birth decision')

    counselling_failure_treatment = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                     string='Counselling regarding failure of treatment?')
    counselling_failure_treatment_decision = fields.Char(tring='Counselling regarding failure of treatment decision')

    counselling_lower_success_rate = fields.Selection(selection=StaticMember.CHOICE_YES_NO_NA,
                                                      string='Counselling regarding lower success '
                                                             'rate with frozen samples?')
    counselling_lower_success_rate_decision = fields.Char(string='Counselling regarding lower success '
                                                                 'rate with frozen samples decision')

    counselling_high_bmi = fields.Selection(selection=StaticMember.CHOICE_YES_NO_NA,
                                            string='Counselling for pregnancies with high BMI?')
    counselling_high_bmi_decision = fields.Char(string='Counselling for pregnancies with high BMI decision')

    def check_field_values_as_red(self):
        no_values = ['no']

        if self.counselling_multiple_birth in no_values:
            return True
        if self.counselling_failure_treatment in no_values:
            return True
        if self.counselling_lower_success_rate in no_values:
            return True
        if self.counselling_high_bmi in no_values:
            return True

        return False
