from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MaleMedicalPhysicalExamination(models.Model):
    _name = "ec.male.physical.examination"
    _description = "Patient (Male) Physical Examination"

    male_physical_examination_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                           ondelete='restrict')

    male_weight = fields.Char('Weight')
    male_height = fields.Char('Height')
    male_bmi = fields.Char('BMI', readonly=True)
    male_bp_upper = fields.Char('B.P')
    male_bp_lower = fields.Char('B.P')
    male_pulse = fields.Char('Pulse')
    male_temperature = fields.Char(string='Temperature')
    male_thyroid_physical = fields.Selection(selection=StaticMember.THYROID,
                                    string='Thyroid')
    male_thyroid_goitear_length = fields.Selection(selection=StaticMember.GOITEAR_LENGTH,
                                                   string='Goitre')
    male_thyroid_goitear_width = fields.Selection(selection=StaticMember.GOITEAR_LENGTH,
                                                  string='Goitre Width')
    male_thyroid_goitear_type = fields.Selection(selection=StaticMember.THYROID_GOITEAR_TYPE,
                                                 string='Goitre Type')

    male_thyroid_goitear_nodule = fields.Boolean(string='Nodule')
    male_pallor = fields.Selection(selection=StaticMember.PALLOR,
                                   string='Pallor')
    male_jaundice = fields.Selection(selection=StaticMember.PALLOR, string='Jaundice')
    male_other_findings = fields.Char(string='Other Findings')
