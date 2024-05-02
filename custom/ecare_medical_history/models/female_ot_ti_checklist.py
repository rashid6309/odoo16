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
    tubal_patency_test_dropdown_decision = fields.Char(string='Tubal Patency Test')

    diagnosis_cervical_incompetence = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    diagnosis_cervical_incompetence_decision = fields.Char(string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                               string='Uterine and Tubal Anomalies Ruled Out?')
    uterine_tubal_anomalies_decision = fields.Char(string='Uterine and Tubal Anomalies Ruled Out?')

    fsh_lh_amh_acceptable = fields.Selection(selection=StaticMember.FSH_LH_AMH_CHOICES,
                                             string='FSH, LH, AMH within acceptable range?')

    menopause_sign_suspicion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Any signs or suspicion of menopause?')
    menopause_sign_suspicion_decision = fields.Char(string='Any signs or suspicion of menopause?')

    female_ot_ti_weight = fields.Char('Weight (kg)')
    female_ot_ti_height = fields.Char('Height (cm)')

    female_ot_ti_bmi = fields.Char(string='BMI Calculation')
    # female_ot_ti_bmi = fields.Char(string='BMI Calculation', compute='_compute_female_ot_ti_bmi')
    female_ot_ti_bmi_decision = fields.Char(string='BMI Calculation')

    tubal_patency_test = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                          string='Tubal Patency Test Indicated?')

    tubal_patency_test_decision = fields.Char(string='Tubal Patency Test Indicated?')

    cervical_incompetence_diagnosis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies_test = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                                    string='Uterine and Tubal Anomalies Ruled Out?')

    oi_ti_decisions = fields.Text('Decisions')
    oi_ti_additional_comments = fields.Text('Additional Comments')
    oi_ti_treatment_prompt_message = fields.Text(readonly="1", string='Message',
                                                 default="One or more contraindications to OI/TI have been "
                                                         "identified and highlighted and therefore, "
                                                         "you cannot authorise OI/TI treatment "
                                                         "pathway for this couple. Proceeding to OI/TI "
                                                         "will have either inappropriate or with poor "
                                                         "prognosis and/or higher risk of complications. "
                                                         "Please discuss it with your seniors.")

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

        female_ot_ti_bmi_value = float(female_ot_ti_bmi_value)
        if float(self.female_ot_ti_bmi) >= female_ot_ti_bmi_value:
            return True

        return False

    # @api.onchange('female_ot_ti_weight', 'female_ot_ti_height')
    # def _compute_female_ot_ti_bmi(self):
    #     for record in self:
    #         if record.female_ot_ti_weight and record.female_ot_ti_height:
    #             height_in_meters = float(record.female_ot_ti_height) / 100
    #             record.female_ot_ti_bmi = round(float(record.female_ot_ti_weight) / (height_in_meters ** 2), 2)
    #         else:
    #             record.female_ot_ti_bmi = None
