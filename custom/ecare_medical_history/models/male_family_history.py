from odoo import models, fields


class MaleFamilyHistory(models.Model):
    _name = 'ec.male.family.history'
    _description = 'Family (Male) History'

    male_family_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                     ondelete='restrict')

    # Male Family History Fields
    male_diabetes_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                         relation='ec_male_family_history_diabetes_rel',
                                         column1='diabetes_id',
                                         column2='ec_male_family_history_id',
                                         string='Diabetes')

    male_other_diabetes = fields.Char(string='Other Details')

    male_malignancies_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='ec_male_family_history_malignancies_rel',
                                             column1='malignancies_id',
                                             column2='ec_male_family_history_id',
                                             string='Malignancies')

    male_other_malignancies = fields.Char(string='Other Details')

    male_hypertension_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='ec_male_family_history_hypertension_rel',
                                             column1='hypertension_id',
                                             column2='ec_male_family_history_id',
                                             string='Hypertension')

    male_other_hypertension = fields.Char(string='Other Details')

    male_mental_illness_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                               relation='ec_male_family_history__mental_illness_rel',
                                               column1='mental_illness_id',
                                               column2='ec_male_family_history_id',
                                               string='Mental Illnesses')
    male_other_mental_illness = fields.Char(string='Other Details')

    male_twins_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                      relation='ec_male_family_history_twins_rel',
                                      column1='twins_id',
                                      column2='ec_male_family_history_id',
                                      string='Multiple Pregnancies')

    male_other_twins = fields.Char(string='Other Details')

    male_tuberculosis_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='ec_male_family_history_tuberculosis_rel',
                                             column1='tuberculosis_id',
                                             column2='ec_male_family_history_id',
                                             string='Tuberculosis')
    male_other_tuberculosis = fields.Char(string='Other Details')

    male_abnormalities_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                              relation='ec_male_family_history_abnormalities_rel',
                                              column1='abnormalities_id',
                                              column2='ec_male_family_history_id',
                                              string='Congenital Abnormalities')

    male_other_abnormalities = fields.Char(string='Other Details')

    male_heart_disease_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                              relation='ec_male_family_history_heart_disease_rel',
                                              column1='ec_male_family_history_id',
                                              column2='heart_disease_id',
                                              string='Heart Disease')

    male_other_heart_disease = fields.Char(string='Other Details')

    male_subfertility_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='ec_male_family_history_subfertility_rel',
                                             column1='ec_male_family_history_id',
                                             column2='subfertility_id',
                                             string='Subfertility')

    male_other_subfertility = fields.Char(string='Other Details')

    male_family_history_other = fields.Char(string='Other History')
