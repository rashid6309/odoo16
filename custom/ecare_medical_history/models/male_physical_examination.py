from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MaleMedicalPhysicalExamination(models.Model):
    _name = "ec.male.physical.examination"
    _description = "Patient (Male) Physical Examination"

    male_weight = fields.Char('Weight')
    male_height = fields.Char('Height')
    male_bmi = fields.Char('BMI')
    male_bp_upper = fields.Char('B.P')
    male_bp_lower = fields.Char('B.P')
    male_pulse = fields.Char('Pulse')
    male_temperature = fields.Char(string='Temperature')
    male_thyroid_physical = fields.Selection(selection=StaticMember.THYROID,
                                    string='Thyroid')
    male_thyroid_goitear_length = fields.Selection(selection=StaticMember.GOITEAR_LENGTH,
                                                   string='Goitear')
    male_thyroid_goitear_width = fields.Selection(selection=StaticMember.GOITEAR_LENGTH,
                                                  string='Goitear Width')
    male_thyroid_goitear_type = fields.Selection(selection=StaticMember.THYROID_GOITEAR_TYPE,
                                                 string='Goitear Type')

    male_thyroid_goitear_nodule = fields.Boolean(string='Nodule')
    male_pallor = fields.Selection(selection=StaticMember.PALLOR,
                                   string='Pallor')
