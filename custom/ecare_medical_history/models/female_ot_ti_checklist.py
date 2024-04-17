from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleOtTiChecklist(models.Model):
    _name = 'female.ot.ti.checklist'
    _description = 'Female Pre OI/TI Checklist'

    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                             string='Repeat Consultation')

    upt_result = fields.Selection(selection=StaticMember.UPT_RESULT,
                                  string='UPT Result?')

    iui_plan = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                string='IUI Currently in Plan?')

    fsh_level = fields.Char(string='FSH')
    lh_level = fields.Char(string='LH')
    amh_level = fields.Char(string='AMH')

    primary_indication = fields.Selection(selection=StaticMember.PRIMARY_INDICATION,
                                          string='Primary Indication')

    tubal_patency_test_dropdown = fields.Selection(selection=StaticMember.IUI_DROPDOWN,
                                    string='Tubal Patency Test')

    diagnosis_cervical_incompetence = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                               string='Uterine and Tubal Anomalies Ruled Out?')

    fsh_lh_amh_acceptable = fields.Selection(selection=StaticMember.FSH_LH_AMH_CHOICES,
                                             string='FSH, LH, AMH within acceptable range?')

    menopause_sign_suspicion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Any signs or suspicion of menopause?')

    female_ot_ti_weight = fields.Float('Weight (kg)')
    female_ot_ti_height = fields.Float('Height (cm)')

    female_ot_ti_bmi = fields.Float(string='BMI Calculation')

    tubal_patency_test = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                          string='Tubal Patency Test Indicated?')

    cervical_incompetence_diagnosis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies_test = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                                    string='Uterine and Tubal Anomalies Ruled Out?')

    oi_ti_decisions = fields.Text('Decisions')
    oi_ti_treatment_state = fields.Char('Treatment State')

    def check_field_values_as_red(self):
        iui_dropdown_red_values = ['not_tested', 'both_blocked', 'restricted_spill']
        uterine_tubal_anomalies_red_values = ['no_testing']

        if self.tubal_patency_test_dropdown in iui_dropdown_red_values:
            return True
        if self.uterine_tubal_anomalies in uterine_tubal_anomalies_red_values:
            return True

        return False

    def check_field_values_as_blue(self):
        yes_values = ['yes']
        female_ot_ti_bmi_value = 35

        if self.diagnosis_cervical_incompetence in yes_values:
            return True
        if self.menopause_sign_suspicion in yes_values:
            return True
        if self.female_ot_ti_bmi >= female_ot_ti_bmi_value:
            return True

        return False


