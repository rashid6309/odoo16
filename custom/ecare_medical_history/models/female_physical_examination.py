from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalPhysicalExamination(models.Model):
    _name = "ec.physical.examination"
    _description = "Patient (Female) Physical Examination"

    female_weight = fields.Char('Weight')
    female_height = fields.Char('Height')
    female_bmi = fields.Char('BMI')
    female_bp_upper = fields.Char('B.P')
    female_bp_lower = fields.Char('B.P')
    female_pulse = fields.Char('Pulse')
    female_temperature = fields.Char('Temperature')
    female_thyroid = fields.Selection(selection=StaticMember.THYROID, string='Thyroid')
    female_thyroid_goitear_length = fields.Selection(selection=StaticMember.GOITEAR_LENGTH, string='Goitear')
    female_thyroid_goitear_width = fields.Selection(selection=StaticMember.GOITEAR_WIDTH, string='Goitear Width')
    female_thyroid_goitear_type = fields.Selection(selection=StaticMember.THYROID_GOITEAR_TYPE, string='Goitear Type')
    female_thyroid_goitear_nodule = fields.Boolean('Nodule')
    female_pallor = fields.Selection(selection=StaticMember.PALLOR, string='Pallor')
