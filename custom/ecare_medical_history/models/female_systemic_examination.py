from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalSystemicExamination(models.Model):
    _name = "ec.female.systemic.examination"
    _description = "Patient (Female) Systemic Examination"

    breast_rt = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Breast (Rt)')
    breast_rt_comment = fields.Char(string='Breast (Rt)')

    breast_lt = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Breast (Lt)')
    breast_lt_comment = fields.Char(string='Breast (Lt)')

    cvs = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='CVS')
    cvs_comment = fields.Char(string='CVS')

    respiratory = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Respiratory')
    respiratory_comment = fields.Char(string='Respiratory')

    abdomen = fields.Selection(selection=StaticMember.ORGAN_SIZE, string='Abdomen')
    abdomen_comment = fields.Char(string='Abdomen')
    other_findings = fields.Char(string='Other Findings')

