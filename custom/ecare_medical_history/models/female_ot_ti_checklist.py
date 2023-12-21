from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleOtTiChecklist(models.Model):
    _name = 'female.ot.ti.checklist'
    _description = 'Female Pre OI/TI Checklist'

    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                             string='Repeat Consultation')

    upt_negative = fields.Selection(selection=StaticMember.UPT_NEGATIVE,
                                    string='UPT Negative?')

    iui_plan = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                string='IUI Currently in Plan?')

    primary_indication = fields.Selection(selection=StaticMember.PRIMARY_INDICATION,
                                          string='Primary Indication')

    iui_dropdown = fields.Selection(selection=StaticMember.IUI_DROPDOWN,
                                    string='Tubal Patency Test')

    diagnosis_cervical_incompetence = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                               string='Uterine and Tubal Anomalies Ruled Out?')

    fsh_lh_amh_acceptable = fields.Selection(selection=StaticMember.FSH_LH_AMH_CHOICES,
                                             string='FSH, LH, AMH within acceptable range?')

    menopause_sign_suspicion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Any signs or suspicion of menopause?')

    bmi = fields.Float(string='BMI Calculation')

    tubal_patency_test = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                          string='Tubal Patency Test Indicated?')

    cervical_incompetence_diagnosis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string='Diagnosis or Risk Factors for Cervical Incompetence?')

    uterine_tubal_anomalies_test = fields.Selection(selection=StaticMember.UTERINE_TUBAL_ANOMALIES,
                                                    string='Uterine and Tubal Anomalies Ruled Out?')


