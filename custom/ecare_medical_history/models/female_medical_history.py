from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleMedicalHistory(models.Model):
    _name = "ec.female.medical.history"
    _description = "Medical (Female) History"

    female_medical_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                         ondelete='restrict')

    male_no_medical_history = fields.Boolean(string='No Significant Medical History')
    female_no_medical_history = fields.Boolean(string='No Significant Medical History')
    # Female-specific fields with the 'female_' prefix
    female_adrenal = fields.Char('Adrenal')
    female_adrenal_date = fields.Many2one("ec.medical.year", 'Adrenal Date')

    female_anti_phospholipid_syndrome = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                     string='Anti-phospholipid Syndrome')

    female_anti_phospholipid_syndrome_date = fields.Many2one("ec.medical.year",'Anti-phospholipid Syndrome Date')

    female_autoimmune_disease = fields.Char('Autoimmune Diseases')
    female_autoimmune_disease_date = fields.Many2one("ec.medical.year",'Autoimmune Diseases Date')

    female_blood_transfusion = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                              string='Blood Transfusion')
    female_blood_transfusion_date = fields.Many2one("ec.medical.year",'Blood Transfusion Date')

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

    female_thyroid_TYPE = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                           string='Thyroid')
    female_thyroid = fields.Text('Thyroid')
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

    ''' not being used '''
    # female_allergies_pr = fields.Text(string='Allergies Pr')
    # female_allergies_pr_d = fields.Date('Allergies Date')
    # female_operations_pr_d = fields.Date('Operations Date')
