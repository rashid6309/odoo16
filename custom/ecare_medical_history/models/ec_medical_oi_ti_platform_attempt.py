from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalOITIPlatform(models.Model):
    _name = "ec.medical.oi.ti.platform.attempt"
    _description = "OI/TI Platform"
    _order = 'create_date desc'

    oi_ti_cycle_day = fields.Integer(string='Cycle Day', related='attempt_cycle_id.cycle_day')
    preparation_method = fields.Selection(selection=StaticMember.PREPARATION_METHOD, string='Preparation Method')
    oi_ti_attempt_state = fields.Selection(selection=StaticMember.OI_TI_ATTEMPT_STATE, string='State',
                                           defult='in_progress')
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
    oi_ti_sign_of_ovulation = fields.Selection(selection=StaticMember.SIGN_OF_OVULATION,
                                               string='Sign of Ovulation')

    oi_ti_cet = fields.Char(string='CET')
    oi_ti_comments = fields.Char(string='Comments')

    #     Inverse Fields
    attempt_cycle_id = fields.Many2one(comodel_name='ec.medical.oi.ti.platform.cycle', ondelete="restrict")
    timeline_id = fields.Many2one(comodel_name='ec.patient.timeline')
    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation')
    
    def action_open_cycle_attempt_form_view(self):
        return {
            "name": "OI/TI Attempt",
            "type": 'ir.actions.act_window',
            "res_model": 'ec.medical.oi.ti.platform.attempt',
            'view_id': self.env.ref('ecare_medical_history.view_ec_medical_oi_ti_platform_attempt_form').id,
            'view_mode': 'form',
            "target": 'new',
            "res_id": self.id,
            'flags': {'initial_mode': 'edit'},
        }

    def create_oi_ti_platform_attempt(self, timeline_id, repeat_consultation_id):
        vals = {
            'timeline_id': timeline_id.id,
            'repeat_consultation_id': repeat_consultation_id.id,
            'oi_ti_follicle_left': repeat_consultation_id.tvs_lov,
            'oi_ti_follicle_right': repeat_consultation_id.tvs_rov,
        }
        oi_ti_platform_attempt = self.env['ec.medical.oi.ti.platform.attempt'].create(vals)
        return oi_ti_platform_attempt

    def create_oi_ti_platform_attempt_from_cycle(self, cycle_id):
        repeat_consultation_id = cycle_id.repeat_consultation_id.id
        oi_ti_attempts = self.env['ec.medical.oi.ti.platform.attempt'].search([
            ('repeat_consultation_id', '=', int(repeat_consultation_id))])
        if oi_ti_attempts:
            # if len(oi_ti_attempts) >= 3:
            #     raise UserError("Three attempts against one OI/TI cycle have already been made, "
            #                     "start a new repeat consultation first.")
            for rec in oi_ti_attempts:
                if rec.oi_ti_attempt_state == 'in_progress':
                    raise UserError("There is a visit already in progress, please complete that first!")

        vals = {
            'timeline_id': cycle_id.cycle_timeline_id.id,
            'repeat_consultation_id': cycle_id.repeat_consultation_id.id,
            'attempt_cycle_id': cycle_id.id,
            'oi_ti_follicle_left': cycle_id.repeat_consultation_id.tvs_lov,
            'oi_ti_follicle_right': cycle_id.repeat_consultation_id.tvs_rov,
            'oi_ti_attempt_state': 'in_progress',
        }
        oi_ti_platform_attempt = self.env['ec.medical.oi.ti.platform.attempt'].create(vals)
        return oi_ti_platform_attempt
