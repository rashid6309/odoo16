from odoo import models, fields


class FemaleGeneralExamination(models.Model):
    _name = 'ec.medical.general.examination'
    _description = "Female General Examination"

    female_marriage = fields.Selection([('first', '1st'),
                                        ('second', '2nd'),
                                        ('third', '3rd'),
                                        ('fourth', '4rth')],
                                       default="first", string='Female Marriage')

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

    MONTHS = [
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('8', '8'),
        ('9', '9'),
        ('10', '10'),
        ('11', '11'),
        ('12', '12'),
    ]

    female_living_duration_years = fields.Integer(string='Living Duration')
    female_living_duration_month = fields.Selection(selection=MONTHS,
                                                    string='Living Duration')

    female_complaints = fields.Selection([('primary_infertility', 'Primary Infertility'),
                                   ('secondary_infertility', 'Secondary Infertility')],
                                  default="primary_infertility", string='complaints')

    # complaints_duration
    female_complaints_duration_years = fields.Integer(string='Complaints Duration')
    female_complaints_duration_month = fields.Selection(selection=MONTHS,
                                                        string='Complaints Duration')

    # years_of_marriage

    female_age_at_marriage = fields.Char(string='Age at Marriage')

    female_parity = fields.Char(string='Parity')







