from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleMedicalHistory(models.Model):
    _name = "ec.female.medical.history"
    _description = "Medical (Female) History"

    # Female-specific fields with the 'female_' prefix
    female_adrenal = fields.Char('Adrenal')
    female_adrenal_date = fields.Date('Adrenal Date')

    female_anti_phospholipid_syndrome = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                     string='Anti-phospholipid Syndrome')

    female_anti_phospholipid_syndrome_date  = fields.Date('Anti-phospholipid Syndrome Date')

    female_autoimmune_disease = fields.Char('Autoimmune Diseases')
    female_autoimmune_disease_date  = fields.Date('Autoimmune Diseases Date')

    female_blood_transfusion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                              string='Blood Transfusion')
    female_blood_transfusion_date = fields.Date('Blood Transfusion Date')

    female_cardiac = fields.Char('Cardiac')
    female_cardiac_date = fields.Date('Cardiac Date')

    female_gall_bladder = fields.Char('Gall Bladder')
    female_gall_bladder_date  = fields.Date('Gall Bladder Date')

    female_gastric = fields.Char('Gastric')
    female_gastric_date = fields.Date('Gastric Date')

    female_gynaecology = fields.Char('Gynecological')
    female_gynaecology_date = fields.Date('Gynecological Date')

    female_haematology = fields.Char('Haematological')
    female_haematology_date = fields.Date('Haematological Date')

    female_intestinal = fields.Char('Intestinal')
    female_intestinal_date = fields.Date('Intestinal Date')

    female_liver = fields.Char('Liver')
    female_liver_date = fields.Date('Liver Date')

    female_low_urinary_tract = fields.Char('Lower Urinary Tract')
    female_low_urinary_tract_date = fields.Date('Lower Urinary Tract Date')

    female_malignancy = fields.Char('Malignancies')
    female_malignancy_date  = fields.Date('Malignancies Date')

    female_neurological = fields.Char('Neurological')
    female_neurological_date = fields.Date('Neurological Date')

    female_renal = fields.Char('Renal')
    female_renal_date = fields.Date('Renal Date')

    female_respiratory = fields.Char('Respiratory')
    female_respiratory_date = fields.Date('Respiratory Date')

    female_skeletal = fields.Char('Skeletal')
    female_skeletal_date = fields.Date('Skeletal Date')

    female_thyroid_TYPE = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                           string='Thyroid')
    female_thyroid = fields.Text('Thyroid')
    female_thyroid_date = fields.Date('Thyroid Date')

    female_heart_disease = fields.Char(string='Heart Disease')
    female_heart_disease_date  = fields.Date('Heart Disease Date')

    female_urinary_infection = fields.Char(string='Urinary Infections')
    female_urinary_infection_date = fields.Date('Urinary Infections Date')

    female_hyper_tension = fields.Char(string='Hypertension Pr')
    female_hyper_tension_date  = fields.Date('Hypertension Date')


    female_janduice = fields.Char(string='Jaundice')
    female_janduice_date = fields.Date('Jaundice Date')

    female_complications_pr = fields.Text(string='Complications')

    female_diabetes = fields.Text(string='Diabetes')
    female_diabetes_type = fields.Selection(selection=StaticMember.DIABETES_TYPE,
                                                 string='Diabetes')
    female_diabetes_date = fields.Date('Diabetes Date')

    female_dvt= fields.Char(string='DVT')
    female_dvt_date = fields.Date('DVT Date')

    female_smoking = fields.Char(string='Smoking')
    female_smoking_date = fields.Date('Smoking Date')

    female_alcohol = fields.Char(string='Alcohol')
    female_alcohol_date = fields.Date(string='Alcohol Date')

    female_operations_pr = fields.Text(string='Operations (if any)')
    female_medical_history_others = fields.Char(string='Others')
    female_medical_history_others_date  = fields.Date('Others Date')

    ''' not being used '''
    # female_allergies_pr = fields.Text(string='Allergies Pr')
    # female_allergies_pr_d = fields.Date('Allergies Date')
    # female_operations_pr_d = fields.Date('Operations Date')
