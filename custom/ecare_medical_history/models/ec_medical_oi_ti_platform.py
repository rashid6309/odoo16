from odoo import models, api, fields


class EcMedicalOITIPlatform(models.Model):
    _name = "ec.medical.oi.ti.platform"
    _description = "OI/TI Platform"
    _order = 'create_date desc'

    oi_ti_left_ovary = fields.Char(string='LEFT OVARY')
    oi_ti_right_ovary = fields.Char(string='Right OVARY')
    oi_ti_diagnosis_ids = fields.Many2many(comodel_name='ec.medical.diagnosis',
                                           relation="ec_medical_oi_ti_diagnosis_rel",
                                           column1="oi_ti_id",
                                           column2="diagnosis_id",
                                           string="Diagnosis")
    oi_ti_other_diagnosis = fields.Char(string='Other Diagnosis')
    oi_ti_follicle_left = fields.Char(string='Follicle(L)')
    oi_ti_follicle_right = fields.Char(string='Follicle(R)')
    oi_ti_cycle_day = fields.Char(string='Cycle Day')
    # oi_ti_sign_of_ovulation_ids = fields.Many2many(comodel_name='ec.medical.diagnosis',
    #                                                relation="ec_medical_oi_ti_diagnosis_rel",
    #                                                column1="oi_ti_id",
    #                                                column2="diagnosis_id",
    #                                                string="Diagnosis")

    oi_ti_cet = fields.Char(string='CET')

#     Inverse Fields
    timeline_id = fields.Many2one(comodel_name='ec.patient.timeline')
    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation')

    def create_oi_ti_platform(self, timeline_id, repeat_consultation_id):
        vals = {
            'timeline_id': timeline_id.id,
            'repeat_consultation_id': repeat_consultation_id.id,
            'oi_ti_follicle_left': repeat_consultation_id.tvs_lov,
            'oi_ti_follicle_right': repeat_consultation_id.tvs_rov,
        }
        oi_ti_platform = self.env['ec.medical.oi.ti.platform'].create(vals)
        return oi_ti_platform
