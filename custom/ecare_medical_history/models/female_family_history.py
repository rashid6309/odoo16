from odoo import models, fields


class FemaleFamilyHistory(models.Model):
    _name = 'ec.female.family.history'
    _description = 'Family (Female) History'

    '''
    # TODO: Change relation name with "ec_female_family_history_diabetes_rel"
    
    '''
    # Female Family History Fields
    female_diabetes_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                           relation='ec_female_family_history_diabetes_rel',
                                           column1='diabetes_id',
                                           column2='ec_female_family_history_id',
                                           string='Diabetes')

    female_other_diabetes = fields.Char(string='Other Details')

    female_malignancies_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                               relation='ec_female_family_history_malignancies_rel',
                                               column1='malignancies_id',
                                               column2='ec_female_family_history_id',
                                               string='Malignancies')

    female_other_malignancies = fields.Char(string='Other Details')

    female_hypertension_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                               relation='ec_female_family_history_hypertension_rel',
                                               column1='hypertension_id',
                                               column2='ec_female_family_history_id',
                                               string='Hypertension')

    female_other_hypertension = fields.Char(string='Other Details')

    female_mental_illness_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                 relation='ec_female_family_history__mental_illness_rel',
                                                 column1='mental_illness_id',
                                                 column2='ec_female_family_history_id',
                                             string='Mental Illnesses')
    female_other_mental_illness = fields.Char(string='Other Details')

    female_twins_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                        relation='ec_female_family_history_twins_rel',
                                        column1='twins_id',
                                        column2='ec_female_family_history_id',
                                    string='Twins')

    female_other_twins = fields.Char(string='Other Details')

    female_tuberculosis_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                               relation='ec_female_family_history_tuberculosis_rel',
                                               column1='tuberculosis_id',
                                               column2='ec_female_family_history_id',
                                               string='Tuberculosis')
    female_other_tuberculosis = fields.Char(string='Other Details')

    female_abnormalities_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                relation='ec_female_family_history_abnormalities_rel',
                                                column1='abnormalities_id',
                                                column2='ec_female_family_history_id',
                                                string='Congenital Abnormalities')

    female_other_abnormalities = fields.Char(string='Other Details')

    female_pregnancy_induced_hypertension_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                                 relation='ec_female_family_history_pregnancy_induce_hypertension_rel',
                                                                 column1='pregnancy_induce_hypertension_id',
                                                                 column2='ec_female_family_history_id',
                                                                 string='Pregnancy Induced Hypertension')
    female_other_pregnancy_induced_hypertension = fields.Char(string='Other Details')

    female_miscarriage_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                              relation='ec_female_family_history_miscarriages_rel',
                                              column1='miscarriages_id',
                                              column2='ec_female_family_history_id',
                                              string='Miscarriages')
    female_other_miscarriage = fields.Char(string='Other Details')

    female_preterm_birth_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                relation='ec_female_family_history_preterm_birth_rel',
                                                column1="preterm_birth_id",
                                                column2='ec_female_family_history_id',
                                                string='Preterm Births')
    female_other_preterm_birth = fields.Char(string='Other Details')

    female_still_birth_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                              relation="ec_female_family_history_still_birth_rel",
                                              column1="still_birth_id",
                                              column2 = 'ec_female_family_history_id',
                                              string='Still Births')
    female_other_still_birth = fields.Char(string='Other Details')

    female_pre_mature_ovarian_failure_ids = fields.Many2many(comodel_name='ec.family.relation.list',
                                                             relation='ec_female_family_history_pre_mature_ovarian_failure_rel',
                                                             column1="pre_mature_ovarian_failure_id",
                                                             column2='ec_female_family_history_id',
                                                             string='Pre-mature Ovarian Failure'
                                                             )

    female_other_pre_mature_ovarian_failure = fields.Char(string='Other Details')
    female_family_history_other = fields.Char(string='Other History')
