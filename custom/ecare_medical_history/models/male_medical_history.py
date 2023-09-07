from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember

''' 
    
    Rename: all the names to the specific
    
'''

class MaleMedicalHistory(models.Model):
    _name = "ec.male.medical.history"
    _description = "Medical (Male) History"

    # Male-specific fields with the 'male_' prefix
    male_adrenal = fields.Char('Adrenal')
    male_adrenal_date = fields.Date('Adrenal Date')

    male_anti_phospholipid_syndrome = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                         string='Anti-phospholipid Syndrome')

    male_anti_phospholipid_syndrome_date  = fields.Date('Anti-phospholipid Syndrome Date')

    male_autoimmune_disease = fields.Char('Autoimmune Diseases')
    male_autoimmune_disease_date  = fields.Date('Autoimmune Diseases Date')

    male_blood_transfusion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                string='Blood Transfusion')
    male_blood_transfusion_date = fields.Date('Blood Transfusion Date')

    male_cardiac = fields.Char('Cardiac')
    male_cardiac_date = fields.Date('Cardiac Date')

    male_gall_bladder = fields.Char('Gall Bladder')
    male_gall_bladder_date  = fields.Date('Gall Bladder Date')

    male_gastric = fields.Char('Gastric')
    male_gastric_date = fields.Date('Gastric Date')

    male_gynaecology = fields.Char('Gynaecological')
    male_gynaecology_date = fields.Date('Gynaecological Date')

    male_haematology = fields.Char('Haematological')
    male_haematology_date = fields.Date('Haematological Date')

    male_intestinal = fields.Char('Intestinal')
    male_intestinal_date = fields.Date('Intestinal Date')

    male_liver = fields.Char('Liver')
    male_liver_date = fields.Date('Liver Date')

    male_low_urinary_tract = fields.Char('Lower Urinary Tract')
    male_low_urinary_tract_date = fields.Date('Lower Urinary Tract Date')

    male_malignancy = fields.Char('Malignancies')
    male_malignancy_date  = fields.Date('Malignancies Date')

    male_neurological = fields.Char('Neurological')
    male_neurological_date = fields.Date('Neurological Date')

    male_renal = fields.Char('Renal')
    male_renal_date = fields.Date('Renal Date')

    male_respiratory = fields.Char('Respiratory')
    male_respiratory_date = fields.Date('Respiratory Date')

    male_skeletal = fields.Char('Skeletal')
    male_skeletal_date = fields.Date('Skeletal Date')

    male_thyroid_TYPE = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                           string='Thyroid')
    male_thyroid = fields.Text('Thyroid')
    male_thyroid_date = fields.Date('Thyroid Date')

    male_heart_disease = fields.Char(string='Heart Disease')
    male_heart_disease_date  = fields.Date('Heart Disease Date')

    male_urinary_infection = fields.Char(string='Urinary Infections')
    male_urinary_infection_date = fields.Date('Urinary Infections Date')

    male_hyper_tension = fields.Char(string='Hypertension Pr')
    male_hyper_tension_date  = fields.Date('Hypertension Date')


    male_janduice = fields.Char(string='Jaundice')
    male_janduice_date = fields.Date('Jaundice Date')

    male_complications_pr = fields.Text(string='Complications')

    male_diabetes = fields.Text(string='Diabetes')
    male_diabetes_type = fields.Selection(selection=StaticMember.DIABETES_TYPE,
                                            string='Diabetes')
    male_diabetes_date = fields.Date('Diabetes Date')

    male_dvt= fields.Char(string='DVT')
    male_dvt_date = fields.Date('DVT Date')

    male_smoking = fields.Char(string='Smoking')
    male_smoking_date = fields.Date('Smoking Date')

    male_alcohol = fields.Char(string='Alcohol')
    male_alcohol_date = fields.Date(string='Alcohol Date')

    male_operations_pr = fields.Text(string='Operations (if any)')
    male_medical_history_others = fields.Char(string='Others')
    male_medical_history_others_date  = fields.Date('Others Date')

    ''' not being used '''
    # male_allergies_pr = fields.Text(string='Allergies Pr')
    # male_allergies_pr_d = fields.Date('Allergies Date')
    # male_operations_pr_d = fields.Date('Operations Date')
