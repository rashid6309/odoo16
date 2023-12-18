from datetime import datetime

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
                                       string='Female Marriage')

    female_comment = fields.Text(string="Details")

    biological_female_dob = fields.Date(string='Biological DOB')
    biological_female_age = fields.Char(string='Female Age', compute='_get_biological_age_female', store=True)

    female_relation = fields.Selection(selection=StaticMember.MARRIAGE_RELATION, string='Relation')

    female_family_system = fields.Selection(selection=StaticMember.FAMILY_LIVING_STYLE, string='Family System')

    female_living_togather = fields.Selection(selection=StaticMember.CHOICE_YES_NO, string='Living Together')

    female_living_togather_reason = fields.Text(string='Reason')

    female_living_duration_years = fields.Selection(selection=StaticMember.YEARS,
                                                    string='Living Duration')
    female_living_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                    string='Living Duration Month')

    female_complaints = fields.Selection(selection=StaticMember.INFERTILITY, string='Complaints')

    # complaints_duration
    female_complaints_duration_years = fields.Selection(selection=StaticMember.YEARS,
                                                        string='Complaints Duration')
    female_complaints_duration_month = fields.Selection(selection=StaticMember.MONTHS,
                                                        string='Complaints Duration Month')

    # years_of_marriage
    female_age_at_marriage = fields.Integer(string='Age at Marriage', compute='calculate_female_age_at_marriage')

    ''' Male Fields '''

    male_marriage = fields.Selection(selection=StaticMember.MARRIAGE,
                                     string="Male Marriage",
                                     )
    male_comment = fields.Char(string="Details")

    biological_male_dob = fields.Date(string='Biological DOB')
    biological_male_age = fields.Char(string='Male Age', compute='_get_biological_age_male', store=True)

    @api.depends('general_history_patient_id.wife_dob', 'general_history_patient_id.married_since')
    def calculate_female_age_at_marriage(self):
        for record in self:
            if record.general_history_patient_id.wife_dob and record.general_history_patient_id.married_since:
                dob = datetime.strptime(str(record.general_history_patient_id.wife_dob), "%Y-%m-%d")
                marriage_date = datetime.strptime(str(record.general_history_patient_id.married_since), "%Y-%m-%d")

                age_at_marriage = (marriage_date - dob).days // 365

                record.female_age_at_marriage = age_at_marriage
            else:
                record.female_age_at_marriage = 0  # Or any default value if the information is missing

