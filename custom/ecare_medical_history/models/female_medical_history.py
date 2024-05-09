from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleMedicalHistory(models.Model):
    _name = "ec.female.medical.history"
    _description = "Medical (Female) History"

    female_medical_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                         ondelete='restrict')

    female_no_medical_history = fields.Boolean(string='No Significant Medical History')
    # Female-specific fields with the 'female_' prefix

    female_acne = fields.Char('Acne')
    female_acne_date = fields.Many2one("ec.medical.year", 'Acne Date')
    female_weight_gain = fields.Char('Weight gain')
    female_weight_gain_year = fields.Many2one("ec.medical.year", 'Over period of (Years)')
    
    female_weight_loss = fields.Char('Weight loss')
    female_weight_loss_year = fields.Many2one("ec.medical.year", 'Over period of (Years)')

    female_weight_at_marriage = fields.Char('Weight at marriage')
    female_weight_comments = fields.Char('Comments')

    female_hirsuitism = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                     string='Hirsuitism')
    female_hirsuitism_year = fields.Many2one("ec.medical.year", 'Hirsuitism')
    female_hirsuitism_treatment = fields.Char('Any treatment')
    female_hirsuitism_comments = fields.Char('Comments')

    female_tuberculosis = fields.Char('Tuberculosis')
    female_tuberculosis_date = fields.Many2one("ec.medical.year", 'Tuberculosis Date')
    female_att_months = fields.Selection(selection=StaticMember.MONTHS_MEDICAL, string='ATT (Months)')
    female_syphilis = fields.Char('Syphilis')
    female_syphilis_date = fields.Many2one("ec.medical.year", 'Syphilis Date')
    female_herpes = fields.Char('Herpes')
    female_herpes_date = fields.Many2one("ec.medical.year", 'Herpes Date')
    female_gonorrhoea = fields.Char('Gonorrhoea')
    female_gonorrhoea_date = fields.Many2one("ec.medical.year", 'Gonorrhoea Date')
    female_hiv = fields.Char('HIV')
    female_hiv_date = fields.Many2one("ec.medical.year", 'HIV Date')
    female_mumps = fields.Char('Mumps')
    female_mumps_date = fields.Many2one("ec.medical.year", 'Mumps Date')

    female_adrenal = fields.Char('Adrenal')
    female_adrenal_date = fields.Many2one("ec.medical.year", 'Adrenal Date')

    female_anti_phospholipid_syndrome = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                         string='Anti-phospholipid Syndrome')
    female_anti_phospholipid_syndrome_comments = fields.Char(string='Anti-phospholipid Syndrome')

    female_anti_phospholipid_syndrome_date = fields.Many2one("ec.medical.year",
                                                             'Anti-phospholipid Syndrome Date')

    female_autoimmune_disease = fields.Char('Autoimmune Diseases')
    female_autoimmune_disease_date = fields.Many2one("ec.medical.year",'Autoimmune Diseases Date')

    female_blood_transfusion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Blood Transfusion')
    female_blood_transfusion_comments = fields.Char('Blood Transfusion')
    female_blood_transfusion_date = fields.Many2one("ec.medical.year",
                                                    'Blood Transfusion Date')

    female_cardiac = fields.Char('Cardiac')
    female_cardiac_date = fields.Many2one("ec.medical.year",'Cardiac Date')

    female_gall_bladder = fields.Char('Gall Bladder')
    female_gall_bladder_date = fields.Many2one("ec.medical.year",'Gall Bladder Date')

    female_gastric = fields.Char('Gastric')
    female_gastric_date = fields.Many2one("ec.medical.year",'Gastric Date')

    female_gynaecology = fields.Char('Gynecological')
    female_gynaecology_date = fields.Many2one("ec.medical.year",'Gynecological Date')

    female_haematology = fields.Char('Haematological')
    female_haematology_date = fields.Many2one("ec.medical.year",'Haematological Date')

    female_intestinal = fields.Char('Intestinal')
    female_intestinal_date = fields.Many2one("ec.medical.year",'Intestinal Date')

    female_liver = fields.Char('Liver')
    female_liver_date = fields.Many2one("ec.medical.year",'Liver Date')

    female_low_urinary_tract = fields.Char('Lower Urinary Tract')
    female_low_urinary_tract_date = fields.Many2one("ec.medical.year",'Lower Urinary Tract Date')

    female_malignancy = fields.Char('Malignancies')
    female_malignancy_date = fields.Many2one("ec.medical.year",'Malignancies Date')

    female_neurological = fields.Char('Neurological')
    female_neurological_date = fields.Many2one("ec.medical.year",'Neurological Date')

    female_renal = fields.Char('Renal')
    female_renal_date = fields.Many2one("ec.medical.year",'Renal Date')

    female_respiratory = fields.Char('Respiratory')
    female_respiratory_date = fields.Many2one("ec.medical.year",'Respiratory Date')

    female_skeletal = fields.Char('Skeletal')
    female_skeletal_date = fields.Many2one("ec.medical.year",'Skeletal Date')

    female_thyroid_type = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                           string='Thyroid')
    female_thyroid_medical = fields.Char('Thyroid')
    female_thyroid_date = fields.Many2one("ec.medical.year",'Thyroid Date')

    female_heart_disease = fields.Char(string='Heart Disease')
    female_heart_disease_date = fields.Many2one("ec.medical.year",'Heart Disease Date')

    female_urinary_infection = fields.Char(string='Urinary Infections')
    female_urinary_infection_date = fields.Many2one("ec.medical.year",'Urinary Infections Date')

    female_hyper_tension = fields.Char(string='Hypertension Pr')
    female_hyper_tension_date = fields.Many2one("ec.medical.year",'Hypertension Date')


    female_janduice = fields.Char(string='Jaundice')
    female_janduice_date = fields.Many2one("ec.medical.year",'Jaundice Date')

    female_complications_pr = fields.Text(string='Complications')

    female_diabetes = fields.Text(string='Diabetes')
    female_diabetes_type = fields.Selection(selection=StaticMember.DIABETES_TYPE,
                                                 string='Diabetes')
    female_diabetes_date = fields.Many2one("ec.medical.year",'Diabetes Date')

    female_dvt= fields.Char(string='DVT')
    female_dvt_date = fields.Many2one("ec.medical.year",'DVT Date')

    female_smoking = fields.Char(string='Smoking')
    female_smoking_date = fields.Many2one("ec.medical.year",'Smoking Date')

    female_alcohol = fields.Char(string='Alcohol')
    female_alcohol_date = fields.Many2one("ec.medical.year",string='Alcohol Date')

    female_operations_pr = fields.Text(string='Operations (if any)')
    female_medical_history_others = fields.Char(string='Others')
    female_medical_history_others_date = fields.Many2one("ec.medical.year",'Others Date')
    female_medical_current_medication = fields.Html(string='Current Medication')
    female_medical_current_allergies = fields.Html(string='Allergies')


    ''' not being used '''
    # female_allergies_pr = fields.Text(string='Allergies Pr')
    # female_allergies_pr_d = fields.Date('Allergies Date')
    # female_operations_pr_d = fields.Date('Operations Date')

    def write(self, vals):
        return super(FemaleMedicalHistory, self).write(vals)
