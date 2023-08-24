from odoo import api, models, fields, _


class FirstConsultation(models.Model):
    _name = 'ec.first.consultation'
    _description = "Patient First Consultation"

    _inherits = {'ec.general.history': 'ec_general_examination_id',
                 'ec.sx.contraception': 'ec_sx_contraception_id',
                 'ec.social.history': 'ec_social_history_id',
                 'ec.gynaecological.history': 'ec_gynaecological_history_id',
                 'ec.female.medical.history': 'ec_female_medical_history_id',
                 'ec.medical.gynaecological.examination': 'ec_medical_gynaecological_examination_id',
                 'ec.physical.examination': 'ec_physical_examination_id',
                 'ec.female.family.history': 'ec_female_family_history_id',
                 'ec.female.systemic.examination': 'ec_female_systemic_examination_id',
                 'ec.genital.examination': 'ec_genital_examination_id', # Male after this
                 'ec.male.physical.examination': 'ec_male_physical_examination_id',
                 'ec.male.systemic.examination': 'ec_male_systemic_examination_id',
                 'ec.male.family.history': 'ec_male_family_history_id',
                 'ec.male.medical.history': 'ec_male_medical_history_id',
                 }

    # Inherits synchronized objects.
    ''' Common '''
    ec_general_examination_id = fields.Many2one(comodel_name="ec.general.history", ondelete='restrict')
    ec_sx_contraception_id = fields.Many2one(comodel_name="ec.sx.contraception", ondelete='restrict')
    ec_social_history_id = fields.Many2one(comodel_name="ec.social.history", ondelete='restrict')

    ''' Female '''
    ec_gynaecological_history_id = fields.Many2one(comodel_name="ec.gynaecological.history", ondelete='restrict')
    ec_female_medical_history_id = fields.Many2one(comodel_name="ec.female.medical.history", ondelete='restrict')

    ec_medical_gynaecological_examination_id = fields.Many2one(comodel_name="ec.medical.gynaecological.examination", ondelete='restrict')
    ec_physical_examination_id = fields.Many2one(comodel_name="ec.physical.examination", ondelete='restrict')
    ec_female_systemic_examination_id = fields.Many2one(comodel_name="ec.female.systemic.examination", ondelete='restrict')
    ec_female_family_history_id = fields.Many2one(comodel_name="ec.female.family.history", ondelete='restrict')

    ''' Female One2many '''
    female_procedures_ids = fields.One2many(comodel_name='ec.patient.procedures',
                                        inverse_name='female_consultation_id',
                                        string="Surgical",
                                        ondelete='restrict')

    obs_history_ids = fields.One2many(comodel_name='ec.obstetrics.history',
                                      inverse_name='first_consultation_id',
                                      string='Obstetrics History',
                                      ondelete='restrict')

    female_lab_history_ids = fields.One2many(comodel_name="ec.lab.history",
                                             inverse_name="female_first_consultation_id",
                                             string="Labs History",
                                             ondelete='restrict')

    ''' Male '''
    ec_genital_examination_id = fields.Many2one(comodel_name="ec.genital.examination", ondelete='restrict')
    ec_male_physical_examination_id = fields.Many2one(comodel_name="ec.male.physical.examination", ondelete='restrict')
    ec_male_systemic_examination_id = fields.Many2one(comodel_name="ec.male.systemic.examination", ondelete='restrict')
    ec_male_family_history_id = fields.Many2one(comodel_name="ec.male.family.history", ondelete='restrict')
    ec_male_medical_history_id = fields.Many2one(comodel_name="ec.male.medical.history", ondelete='restrict')

    ''' Male One2Many'''

    male_procedures_ids = fields.One2many(comodel_name='ec.patient.procedures',
                                            inverse_name='male_consultation_id',
                                            string="Surgical",
                                            ondelete='restrict')

    male_lab_history_ids = fields.One2many(comodel_name="ec.lab.history", inverse_name="male_first_consultation_id")

    ''' Normal attributes '''
    name = fields.Char(string='Name')

    ''' One2Many'''

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 required=True)
