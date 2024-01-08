from odoo import models, fields
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MaleSystemicExam(models.Model):
    _name = 'ec.male.systemic.examination'
    _description = "Male Systemic Examination"


    male_systemic_examination_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                           ondelete='restrict')

    male_cvs = fields.Selection(selection=StaticMember.ORGAN_SIZE, string="CVS")
    male_cvs_comment = fields.Char(string="Comment")

    male_respiratory_systematic = fields.Selection(selection=StaticMember.ORGAN_SIZE, string="Respiratory")
    male_respiratory_comment = fields.Char(string="Comment")
    male_abdomen = fields.Selection(selection=StaticMember.ORGAN_SIZE, string="Abdomen")
    male_abdomen_comment = fields.Char(string="Comment")

    male_systemic_other = fields.Char(string="Other Findings")

