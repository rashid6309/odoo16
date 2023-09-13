from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


''' Copied from the female and just changed the attributes names '''


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
    male_thyroid = fields.Selection(selection=StaticMember.THYROID,
                                    string='Thyroid')
    male_thyroid_goitear_length = fields.Char(string='Goitear')
    male_thyroid_goitear_width = fields.Char(string='Goitear')
    male_thyroid_goitear_type = fields.Selection(selection=StaticMember.THYROID_GOITEAR_TYPE,
                                                 string='Goitear')

    male_thyroid_goitear_nodule = fields.Boolean(string='Nodule')
    male_pallor = fields.Selection(selection=StaticMember.PALLOR,
                                   string='Pallor')
