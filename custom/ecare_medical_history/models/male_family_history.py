from odoo import models, fields

"""

    # For male:
    # TODO: Change relation name with "ec_male_family_history_diabetes_rel"
"""

class MaleFamilyHistory(models.Model):
    _name = 'ec.male.family.history'
    _description = 'Family (Male) History'

    # Male Family History Fields
    male_diabetes_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                         relation='male_diabetes_rel',
                                         column1='male_family_history_id',
                                         column2='diabetes_id',
                                         string='Diabetes')

    male_other_diabetes = fields.Char(string='Other Details')

    male_malignancies_ids = fields.Many2many('ec.family.relation.list',
                                             relation='male_malignancies_rel',
                                             column1='name',
                                             column2='malignancies_id',
                                             string='Malignancies')
    male_other_malignancies = fields.Char(string='Other Details')

    male_hypertension_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='male_hypertension_rel',
                                             column1='name',
                                             column2='hypertension_id',
                                             string='Hypertension')
    male_other_hypertension = fields.Char(string='Other Details')

    male_mental_illness_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                               relation='male_mental_illness_rel',
                                               column1='name',
                                               column2='mental_illness_id',
                                               string='Mental Illnesses')
    male_other_mental_illness = fields.Char(string='Other Details')

    male_twins_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                      relation='male_twins_ids',
                                      column1='name',
                                      column2='fhx_twins_id',
                                      string='Twins')
    male_other_twins = fields.Char(string='Other Details')

    male_tuberculosis_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                             relation='male_tuberculosis_rel',
                                             column1='tuberculosis_id',
                                             column2='name',
                                             string='Tuberculosis')
    male_other_tuberculosis = fields.Char(string='Other Details')

    male_c_abnormalities_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                relation='male_abnormalities_rel',
                                                column1='c_abnormalities_id',
                                                column2='name',
                                                string='Congenital Abnormalities')
    male_other_c_abnormalities = fields.Char(string='Other Details')

    male_pih_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                    relation='male_pih_rel',
                                    column1='pih_id',
                                    column2='name',
                                    string='Pregnancy Induced Hypertension')
    male_other_pih = fields.Char(string='Other Details')

    male_misscarriages_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                              relation='male_misscarriages_rel',
                                              column1='misscarriages_id',
                                              column2='name',
                                              string='Miscarriages')
    male_other_misscarriages = fields.Char(string='Other Details')

    male_pb_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                   relation='male_pb_rel',
                                   column1='pb_id',
                                   column2='name',
                                   string='Preterm Births')
    male_other_pb = fields.Char(string='Other Details')

    male_sb_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                   relation='male_sb_rel',
                                   column1='sb_id',
                                   column2='name',
                                   string='Still Births')
    male_other_sb = fields.Char(string='Other Details')

    male_pmof_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                     relation='male_pmof_rel',
                                     column1='pmof_id',
                                     column2='name',
                                     string='Pre-mature Ovarian Failure')

    male_other_pmof = fields.Char(string='Other Details')
    male_other_history = fields.Char(string='Other History')
