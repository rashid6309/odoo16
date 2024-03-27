from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember

''' 
    
    Rename: all the names to the specific
    
'''


class MaleMedicalHistory(models.Model):
    _name = "ec.male.medical.history"
    _description = "Medical (Male) History"

    # Male-specific fields with the 'male_' prefix

    ''' Common '''
    male_medical_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                        ondelete='restrict')

    male_acne = fields.Char('Acne')
    male_acne_date = fields.Many2one("ec.medical.year", 'Acne Date')
    male_weight_gain = fields.Char('Weight gain')
    male_weight_gain_year = fields.Many2one("ec.medical.year", 'Over period of (Years)')

    male_weight_loss = fields.Char('Weight loss')
    male_weight_loss_year = fields.Many2one("ec.medical.year", 'Over period of (Years)')

    male_weight_at_marriage = fields.Char('Weight at marriage')
    male_weight_comments = fields.Char('Comments')

    male_hirsuitism = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                         string='Hirsuitism')
    male_hirsuitism_treatment = fields.Char('Any treatment')

    male_tuberculosis = fields.Char('Tuberculosis')
    male_tuberculosis_date = fields.Many2one("ec.medical.year", 'Tuberculosis Date')
    male_att_months = fields.Selection(selection=StaticMember.MONTHS_MEDICAL, string='ATT (Months)')
    male_syphilis = fields.Char('Syphilis')
    male_syphilis_date = fields.Many2one("ec.medical.year", 'Syphilis Date')
    male_herpes = fields.Char('Herpes')
    male_herpes_date = fields.Many2one("ec.medical.year", 'Herpes Date')
    male_gonorrhoea = fields.Char('Gonorrhoea')
    male_gonorrhoea_date = fields.Many2one("ec.medical.year", 'Gonorrhoea Date')
    male_hiv = fields.Char('HIV')
    male_hiv_date = fields.Many2one("ec.medical.year", 'HIV Date')
    male_mumps = fields.Char('Mumps')
    male_mumps_date = fields.Many2one("ec.medical.year", 'Mumps Date')

    male_adrenal = fields.Char('Adrenal')
    male_adrenal_date = fields.Many2one("ec.medical.year", 'Adrenal Date')

    male_anti_phospholipid_syndrome = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                         string='Anti-phospholipid Syndrome')

    male_anti_phospholipid_syndrome_date = fields.Many2one("ec.medical.year", 'Anti-phospholipid Syndrome Date')

    male_autoimmune_disease = fields.Char('Autoimmune Diseases')
    male_autoimmune_disease_date = fields.Many2one("ec.medical.year", 'Autoimmune Diseases Date')

    male_blood_transfusion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Blood Transfusion')
    male_blood_transfusion_date = fields.Many2one("ec.medical.year", 'Blood Transfusion Date')

    male_cardiac = fields.Char('Cardiac')
    male_cardiac_date = fields.Many2one("ec.medical.year", 'Cardiac Date')

    male_gall_bladder = fields.Char('Gall Bladder')
    male_gall_bladder_date = fields.Many2one("ec.medical.year", 'Gall Bladder Date')

    male_gastric = fields.Char('Gastric')
    male_gastric_date = fields.Many2one("ec.medical.year", 'Gastric Date')

    male_gynaecology = fields.Char('Gynecological')
    male_gynaecology_date = fields.Many2one("ec.medical.year", 'Gynecological Date')

    male_haematology = fields.Char('Haematological')
    male_haematology_date = fields.Many2one("ec.medical.year", 'Haematological Date')

    male_intestinal = fields.Char('Intestinal')
    male_intestinal_date = fields.Many2one("ec.medical.year", 'Intestinal Date')

    male_liver = fields.Char('Liver')
    male_liver_date = fields.Many2one("ec.medical.year", 'Liver Date')

    male_low_urinary_tract = fields.Char('Lower Urinary Tract')
    male_low_urinary_tract_date = fields.Many2one("ec.medical.year", 'Lower Urinary Tract Date')

    male_malignancy = fields.Char('Malignancies')
    male_malignancy_date = fields.Many2one("ec.medical.year", 'Malignancies Date')

    male_neurological = fields.Char('Neurological')
    male_neurological_date = fields.Many2one("ec.medical.year", 'Neurological Date')

    male_renal = fields.Char('Renal')
    male_renal_date = fields.Many2one("ec.medical.year", 'Renal Date')

    male_respiratory = fields.Char('Respiratory')
    male_respiratory_date = fields.Many2one("ec.medical.year", 'Respiratory Date')

    male_skeletal = fields.Char('Skeletal')
    male_skeletal_date = fields.Many2one("ec.medical.year", 'Skeletal Date')

    male_thyroid_TYPE = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                         string='Thyroid')
    male_thyroid_medical = fields.Char('Thyroid')
    male_thyroid_date = fields.Many2one("ec.medical.year", 'Thyroid Date')

    male_heart_disease = fields.Char(string='Heart Disease')
    male_heart_disease_date = fields.Many2one("ec.medical.year", 'Heart Disease Date')

    male_urinary_infection = fields.Char(string='Urinary Infections')
    male_urinary_infection_date = fields.Many2one("ec.medical.year", 'Urinary Infections Date')

    male_hyper_tension = fields.Char(string='Hypertension Pr')
    male_hyper_tension_date = fields.Many2one("ec.medical.year", 'Hypertension Date')


    male_janduice = fields.Char(string='Jaundice')
    male_janduice_date = fields.Many2one("ec.medical.year", 'Jaundice Date')

    male_complications_pr = fields.Text(string='Complications')

    male_diabetes = fields.Text(string='Diabetes')
    male_diabetes_type = fields.Selection(selection=StaticMember.DIABETES_TYPE,
                                            string='Diabetes')
    male_diabetes_date = fields.Many2one("ec.medical.year", 'Diabetes Date')

    male_dvt = fields.Char(string='DVT')
    male_dvt_date = fields.Many2one("ec.medical.year", 'DVT Date')

    male_smoking = fields.Char(string='Smoking')
    male_smoking_date = fields.Many2one("ec.medical.year", 'Smoking Date')

    male_alcohol = fields.Char(string='Alcohol')
    male_alcohol_date = fields.Many2one("ec.medical.year", string='Alcohol Date')

    male_operations_pr = fields.Text(string='Operations (if any)')
    male_medical_history_others = fields.Char(string='Others')
    male_medical_history_others_date = fields.Many2one("ec.medical.year", 'Others Date')
    male_medical_current_medication = fields.Html(string='Current Medication')

    ''' not being used '''
    # male_allergies_pr = fields.Text(string='Allergies Pr')
    # male_allergies_pr_d = fields.Date('Allergies Date')
    # male_operations_pr_d = fields.Date('Operations Date')
