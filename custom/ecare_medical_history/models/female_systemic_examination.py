from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalSystemicExamination(models.Model):
    _name = "ec.female.systemic.examination"
    _description = "Patient (Female) Systemic Examination"

    breast_right = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Breast (Rt)')
    breast_right_comment = fields.Char(string='Breast (Rt)')

    breast_left = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Breast (Lt)')
    breast_left_comment = fields.Char(string='Breast (Lt)')

    cvs = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='CVS')
    cvs_comment = fields.Char(string='CVS Comments')

    respiratory = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Respiratory')
    respiratory_comment = fields.Char(string='Respiratory Comment')

    abdomen = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Abdomen')
    abdomen_comment = fields.Char(string='Abdomen Comment')
    other_findings = fields.Text(string='Other Findings')

