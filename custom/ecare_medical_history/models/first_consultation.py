from odoo import api, models, fields, _


class FirstConsultation(models.Model):
    _name = 'ec.first.consultation'
    _description = "Patient First Consultation"

    _inherits = {'ec.general.history': 'ec_general_examination_id',
                 'ec.obstetrics.history': 'ec_obstetrics_history_id',
                 'ec.gynaecological.history': 'ec_gynaecological_history_id',
                 'ec.medical.history': 'ec_medical_history_id',
                 'ec.medical.gynaecological.examination': 'ec_medical_gynaecological_examination_id',
                 'ec.physical.examination': 'ec_physical_examination_id',
                 'ec.systematic.examination': 'ec_systematic_examination_id',
                 'ec.genital.examination': 'ec_genital_examination_id', # Male after this
                 'ec.male.physical.examination': 'ec_male_physical_examination_id',
                 'ec.male.systemic.examination': 'ec_male_systemic_examination_id',
                 }

    # Inherits synchronized objects.
    # Female
    ec_general_examination_id = fields.Many2one(comodel_name="ec.general.history")
    ec_obstetrics_history_id = fields.Many2one(comodel_name="ec.obstetrics.history")
    ec_gynaecological_history_id = fields.Many2one(comodel_name="ec.gynaecological.history")
    ec_social_history_id = fields.Many2one(comodel_name="ec.social.history")
    ec_medical_history_id = fields.Many2one(comodel_name="ec.medical.history")

    ec_medical_gynaecological_examination_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination")
    ec_physical_examination_id = fields.Many2one(comodel_name="ec.physical.examination")
    ec_medical_systematic_examination_id = fields.Many2one(comodel_name="ec.systematic.examination")

    pat_procedures = fields.One2many(comodel_name='ec.medical.patient.procedures', inverse_name='procedure_id')

    # Male
    ec_genital_examination_id = fields.Many2one(comodel_name="ec.genital.examination")
    ec_male_physical_examination_id = fields.Many2one(comodel_name="ec.male.physical.examination")
    ec_male_systemic_examination_id = fields.Many2one(comodel_name="ec.male.systemic.examination")


    # Normal Attributes
    name = fields.Char(string='Name')

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 required=True)

    obs_history_ids = fields.One2many(comodel_name='ec.obstetrics.history',
                                      inverse_name='consultation_id',
                                      string='Obstetrics History')

    # Female Family History Fields
    female_diabetes = fields.Many2many('ec.medical.patient.family.history', 'fhx_diabetes', 'name', 'diabetes_id',
                                       string='Diabetes')
    female_other_diabetes = fields.Char(string='Other Details')
    female_malignancies = fields.Many2many('ec.medical.patient.family.history', 'fhx_malignancies', 'name',
                                           'malignancies_id',
                                           string='Malignancies')
    female_other_malignancies = fields.Char(string='Other Details')
    female_hypertension = fields.Many2many('ec.medical.patient.family.history', 'fhx_hypertension', 'name',
                                           'hypertension_id',
                                           string='Hypertension')
    female_other_hypertension = fields.Char(string='Other Details')
    female_mental_illness = fields.Many2many('ec.medical.patient.family.history', 'fhx_mental_illness', 'name',
                                             'mental_illness_id',
                                             string='Mental Illnesses')
    female_other_mental_illness = fields.Char(string='Other Details')
    female_twins = fields.Many2many('ec.medical.patient.family.history', 'fhx_twins', 'name', 'fhx_twins_id',
                                    string='Twins')
    female_other_twins = fields.Char(string='Other Details')
    female_tuberculosis = fields.Many2many('ec.medical.patient.family.history', 'fhx_tuberculosis', 'tuberculosis_id',
                                           'name',
                                           string='Tuberculosis')
    female_other_tuberculosis = fields.Char(string='Other Details')
    female_c_abnormalities = fields.Many2many('ec.medical.patient.family.history',
                                              'fhx_c_abnormalities', 'c_abnormalities_id', 'name',
                                              string='Congenital Abnormalities')
    female_other_c_abnormalities = fields.Char(string='Other Details')
    female_pih = fields.Many2many('ec.medical.patient.family.history',
                                  'fhx_pih', 'pih_id', 'name',
                                  string='Pregnancy Induced Hypertension')
    female_other_pih = fields.Char(string='Other Details')
    female_misscarriages = fields.Many2many('ec.medical.patient.family.history',
                                            'fhx_misscarriages', 'misscarriages_id', 'name',
                                            string='Miscarriages')
    female_other_misscarriages = fields.Char(string='Other Details')
    female_pb = fields.Many2many('ec.medical.patient.family.history',
                                 'fhx_pb', 'pb_id', 'name',
                                 string='Preterm Births')
    female_other_pb = fields.Char(string='Other Details')
    female_sb = fields.Many2many('ec.medical.patient.family.history',
                                 'fhx_sb', 'sb_id', 'name',
                                 string='Still Births')
    female_other_sb = fields.Char(string='Other Details')
    female_pmof = fields.Many2many('ec.medical.patient.family.history',
                                   'fhx_pmof', 'pmof_id', 'name',
                                   string='Pre-mature Ovarian Failure')
    female_other_pmof = fields.Char(string='Other Details')
    female_other_history = fields.Char(string='Other History')
