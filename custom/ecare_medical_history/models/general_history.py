from odoo import models, api, fields, _


from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GeneralExamination(models.Model):
    _name = 'ec.general.history'
    _description = "General Examination"

    ''' Common '''

    general_history_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 ondelete='restrict')

    ''' Female data-members'''

    female_marriage = fields.Selection(selection=StaticMember.MARRIAGE,
                                       default="first",
                                       string='Female Marriage')

    female_comment = fields.Text(string="Details")

    biological_female_dob = fields.Date(string='Biological DOB')
    biological_female_age = fields.Char(string='Age', compute='_get_biological_age_female', store=True)

    female_relation = fields.Selection(selection=StaticMember.MARRIAGE_RELATION,
                                default="first_cousin", string='Relation')

    female_family_system = fields.Selection(selection=StaticMember.FAMILY_LIVING_STYLE,
                                     default="joint", string='Family System')

    female_living_togather = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                       default="yes", string='Living Together')

    female_living_togather_reason = fields.Text(string='Reason')

    female_living_duration_years = fields.Integer(string='Living Duration Years')
    female_living_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                    string='Living Duration Month')

    female_complaints = fields.Selection(selection=StaticMember.INFERTILITY,
                                  default="primary_infertility", string='Complaints')

    # complaints_duration
    female_complaints_duration_years = fields.Integer(string='Complaints Duration Year')
    female_complaints_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                        string='Complaints Duration Month')

    # years_of_marriage
    female_age_at_marriage = fields.Char(string='Age at Marriage')

    female_parity = fields.Char(string='Parity')

    ''' Male Fields '''

    male_marriage = fields.Selection(selection=StaticMember.MARRIAGE,
                                     string="Male Marriage",
                                     )
    male_comment = fields.Char(string="Details")

    biological_male_dob = fields.Date(string='Biological DOB')
    biological_male_age = fields.Char(string='Age', compute='_get_biological_age_male', store=True)