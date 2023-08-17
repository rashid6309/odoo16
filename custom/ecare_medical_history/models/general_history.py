from odoo import models, fields

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GeneralExamination(models.Model):
    _name = 'ec.general.history'
    _description = "Female General Examination"

    ''' Static attributes '''

    ''' Common '''

    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 ondelete='restrict')

    ''' Female data-members'''

    female_marriage = fields.Selection(selection=StaticMember.MARRIAGE,
                                       default="first",
                                       string='Female Marriage')

    female_age = fields.Char(string="Female Age",
                             related="patient_id.wife_age")

    female_relation = fields.Selection([('first_cousin', '1st Cousin'),
                                 ('second_cousin', '2nd Cousin'),
                                 ('distant_relatives', 'Distant Relatives'),
                                 ('not_related', 'Not Related')],
                                default="first_cousin", string='Relation')

    female_family_system = fields.Selection([('joint', 'Joint'),
                                      ('independent', 'Independent')],
                                     default="joint", string='Family System')

    female_living_togather = fields.Selection([('yes', 'Yes'),
                                        ('no', 'No')],
                                       default="yes", string='Living Togather')

    female_living_togather_reason = fields.Char(string='Living Togather')

    female_living_duration_years = fields.Integer(string='Living Duration')
    female_living_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                    string='Living Duration')

    female_complaints = fields.Selection([('primary_infertility', 'Primary Infertility'),
                                   ('secondary_infertility', 'Secondary Infertility')],
                                  default="primary_infertility", string='complaints')

    # complaints_duration
    female_complaints_duration_years = fields.Integer(string='Complaints Duration')
    female_complaints_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                        string='Complaints Duration')

    # years_of_marriage

    female_age_at_marriage = fields.Char(string='Age at Marriage')

    female_parity = fields.Char(string='Parity')


    ''' Male Fields '''

    male_marriage = fields.Selection(selection=StaticMember.MARRIAGE,
                                     string="Male Marriage",
                                     )

    male_comment = fields.Char(string="Details")
    male_age = fields.Char(related="patient_id.husband_age",
                           string="Age")





