from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MaleMedicalHistory(models.Model):
    _name = "ec.male.medical.history"
    _description = "Medical (Male) History"

    # Male-specific fields with the 'male_' prefix
    male_adrenal_pr = fields.Char('Adrenal')

    male_ant_pr = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                     string='Anti-phospholipid Syndrome')

    male_aut_pr = fields.Char('Autoimmune Diseases')
    male_car_pr = fields.Char('Cardiac')
    male_gal_pr = fields.Char('Gall Bladder')
    male_gas_pr = fields.Char('Gastric')
    male_gyn_pr = fields.Char('Gynaecological')
    male_hae_pr = fields.Char('Haematological')
    male_int_pr = fields.Char('Intestinal')
    male_liver_pr = fields.Char('Liver')
    male_low_pr = fields.Char('Lower Urinary Tract')
    male_mal_pr = fields.Char('Malignancies Pr')
    male_neu_pr = fields.Char('Neurological')
    male_renal_pr = fields.Char('Renal')
    male_res_pr = fields.Char('Respiratory')
    male_ske_pr = fields.Char('Skeletal')
    male_thy_pr = fields.Text('Thyroid Pr')
    male_thy_select_pr = fields.Selection(selection=StaticMember.MEDICAL_THYROID,
                                            string='Thyroid')
    male_hdisease_pr = fields.Char(string='Heart Disease')
    male_uinfact_pr = fields.Char(string='Urinary Infections')
    male_htension_pr = fields.Char(string='Hypertension Pr')
    male_allergies_pr = fields.Text(string='Allergies Pr')
    male_btransfusion_pr = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                            string='Blood Transfusion')
    male_janduice_pr = fields.Char(string='Jaundice')
    male_complications_pr = fields.Text(string='Complications')
    male_diabetes_pr = fields.Text(string='Diabetes Pr')
    male_diabetes_select_pr = fields.Selection(selection=StaticMember.DIABETES_TYPE,
                                                 string='Diabetes')
    male_dvt_pr = fields.Char(string='DVT')
    male_saa_pr = fields.Char(string='Smoking')
    male_alcohol_pr = fields.Char(string='Alcohol')
    male_alcohol_pr_d = fields.Date(string='Alcohol Date')
    male_operations_pr = fields.Text(string='Operations (if any)')
    male_others_pr = fields.Char(string='Others')

    # Dates relevant to fields
    male_adrenal_pr_d = fields.Date('Adrenal Date')
    male_allergies_pr_d = fields.Date('Allergies Date')
    male_ant_pr_d = fields.Date('Anti-phospholipid Syndrome Date')
    male_aut_pr_d = fields.Date('Autoimmune Diseases Date')
    male_btransfusion_pr_d = fields.Date('Blood Transfusion Date')
    male_car_pr_d = fields.Date('Cardiac Date')
    male_diabetes_pr_d = fields.Date('Diabetes Date')
    male_dvt_pr_d = fields.Date('DVT Date')
    male_gal_pr_d = fields.Date('Gall Bladder Date')
    male_gas_pr_d = fields.Date('Gastric Date')
    male_gyn_pr_d = fields.Date('Gynaecological Date')
    male_hae_pr_d = fields.Date('Haematological Date')
    male_hdisease_pr_d = fields.Date('Heart Disease Date')
    male_htension_pr_d = fields.Date('Hypertension Date')
    male_int_pr_d = fields.Date('Intestinal Date')
    male_janduice_pr_d = fields.Date('Jaundice Date')
    male_liver_pr_d = fields.Date('Liver Date')
    male_low_pr_d = fields.Date('Lower Urinary Tract Date')
    male_mal_pr_d = fields.Date('Malignancies Date')
    male_neu_pr_d = fields.Date('Neurological Date')
    male_renal_pr_d = fields.Date('Renal Date')
    male_res_pr_d = fields.Date('Respiratory Date')
    male_saa_pr_d = fields.Date('Smoking Date')
    male_ske_pr_d = fields.Date('Skeletal Date')
    male_thy_pr_d = fields.Date('Thyroid Date')
    male_uinfact_pr_d = fields.Date('Urinary Infections Date')
    male_operations_pr_d = fields.Date('Operations Date')
    male_others_pr_d = fields.Date('Others Date')
