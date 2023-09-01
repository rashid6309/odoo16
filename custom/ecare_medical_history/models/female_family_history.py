from odoo import models, fields


class FemaleFamilyHistory(models.Model):
    _name = 'ec.female.family.history'
    _description = 'Family (Female) History'

    '''
    # TODO: Change relation name with "ec_female_family_history_diabetes_rel"
    # For male:
    # TODO: Change relation name with "ec_male_family_history_diabetes_rel"
    
    '''
    # Female Family History Fields
    female_diabetes_ids = fields.Many2many('ec.family.relation.list', 'fhx_diabetes', 'name', 'diabetes_id',
                                       string='Diabetes')
    female_other_diabetes = fields.Char(string='Other Details')

    female_malignancies_ids = fields.Many2many('ec.family.relation.list', 'fhx_malignancies', 'name',
                                           'malignancies_id',
                                           string='Malignancies')
    female_other_malignancies = fields.Char(string='Other Details')

    female_hypertension_ids = fields.Many2many('ec.family.relation.list', 'fhx_hypertension', 'name',
                                           'hypertension_id',
                                           string='Hypertension')
    female_other_hypertension = fields.Char(string='Other Details')

    female_mental_illness_ids = fields.Many2many('ec.family.relation.list', 'fhx_mental_illness', 'name',
                                             'mental_illness_id',
                                             string='Mental Illnesses')
    female_other_mental_illness = fields.Char(string='Other Details')

    female_twins_ids = fields.Many2many('ec.family.relation.list', 'fhx_twins', 'name', 'fhx_twins_id',
                                    string='Twins')
    female_other_twins = fields.Char(string='Other Details')

    female_tuberculosis_ids = fields.Many2many('ec.family.relation.list', 'fhx_tuberculosis', 'tuberculosis_id',
                                           'name',
                                           string='Tuberculosis')
    female_other_tuberculosis = fields.Char(string='Other Details')

    female_c_abnormalities_ids = fields.Many2many('ec.family.relation.list',
                                              'fhx_c_abnormalities', 'c_abnormalities_id', 'name',
                                              string='Congenital Abnormalities')
    female_other_c_abnormalities = fields.Char(string='Other Details')

    female_pih_ids = fields.Many2many('ec.family.relation.list',
                                  'fhx_pih', 'pih_id', 'name',
                                  string='Pregnancy Induced Hypertension')
    female_other_pih = fields.Char(string='Other Details')

    female_misscarriages_ids = fields.Many2many('ec.family.relation.list',
                                            'fhx_misscarriages', 'misscarriages_id', 'name',
                                            string='Miscarriages')
    female_other_misscarriages = fields.Char(string='Other Details')

    female_pb_ids = fields.Many2many('ec.family.relation.list',
                                 'fhx_pb', 'pb_id', 'name',
                                 string='Preterm Births')
    female_other_pb = fields.Char(string='Other Details')

    female_sb_ids = fields.Many2many('ec.family.relation.list',
                                 'fhx_sb', 'sb_id', 'name',
                                 string='Still Births')
    female_other_sb = fields.Char(string='Other Details')

    female_pmof_ids = fields.Many2many('ec.family.relation.list',
                                   'fhx_pmof', 'pmof_id', 'name',
                                   string='Pre-mature Ovarian Failure')

    female_other_pmof = fields.Char(string='Other Details')
    female_other_history = fields.Char(string='Other History')
