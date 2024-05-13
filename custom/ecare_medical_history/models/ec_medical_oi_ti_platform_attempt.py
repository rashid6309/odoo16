from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalOITIPlatform(models.Model):
    _name = "ec.medical.oi.ti.platform.attempt"
    _description = "OI/TI Platform"
    _order = 'create_date desc'
    _inherits = {
        'ec.medical.tvs': 'ot_ti_visit_tvs_id'
    }

    ot_ti_visit_tvs_id = fields.Many2one(comodel_name="ec.medical.tvs")

    oi_ti_cycle_day = fields.Integer(string='Cycle Day', related='attempt_cycle_id.cycle_day')
    lmp_date = fields.Date(string='LMP', compute='_compute_visit_values')
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
    oi_ti_follicle_left = fields.Char(string='Follicle(L)', compute='_compute_visit_ultrasound_values')
    oi_ti_follicle_right = fields.Char(string='Follicle(R)', compute='_compute_visit_ultrasound_values')
    oi_ti_sign_of_ovulation = fields.Selection(selection=StaticMember.SIGN_OF_OVULATION,
                                               string='Sign of Ovulation')

    oi_ti_cyst_computed = fields.Html(string='Cyst', compute='_compute_visit_ultrasound_values')

    oi_ti_cet = fields.Char(string='CET', compute='_compute_visit_ultrasound_values')
    oi_ti_endometrial_character = fields.Char(string='Endometrial Character', compute='_compute_visit_ultrasound_values')
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
        oi_ti_attempts = self.env['ec.medical.oi.ti.platform.cycle'].search([
            ('repeat_consultation_id', '=', int(repeat_consultation_id))])
        oi_ti_visits = self.env['ec.medical.oi.ti.platform.attempt'].search([
            ('attempt_cycle_id', '=', int(cycle_id.id))], order='write_date desc', limit=1)
        val_preparation_method = None
        if oi_ti_visits:
            val_preparation_method = oi_ti_visits.preparation_method

        # if oi_ti_attempts:
        #     # if len(oi_ti_attempts) >= 3:
        #     #     raise UserError("Three attempts against one OI/TI cycle have already been made, "
        #     #                     "start a new repeat consultation first.")
        #     for rec in oi_ti_attempts:
        #         if rec.oi_ti_platform in ['ready_to_trigger', '2nd_trigger', 'luteal_phase']:
        #             raise UserError("There is a cycle already in progress, please complete that first!")

        vals = {
            'timeline_id': cycle_id.cycle_timeline_id.id,
            'repeat_consultation_id': cycle_id.repeat_consultation_id.id,
            'preparation_method': val_preparation_method or None,
            'attempt_cycle_id': cycle_id.id,
            'oi_ti_follicle_left': cycle_id.repeat_consultation_id.tvs_lov,
            'oi_ti_follicle_right': cycle_id.repeat_consultation_id.tvs_rov,
            'oi_ti_attempt_state': 'in_progress',
            'ot_ti_visit_tvs_id': cycle_id.repeat_consultation_id.repeat_tvs_id.id if not oi_ti_attempts else None,
        }
        oi_ti_platform_attempt = self.env['ec.medical.oi.ti.platform.attempt'].create(vals)
        return oi_ti_platform_attempt

        # return {
        #     'type': 'ir.actions.act_window',
        #     'name': 'OI/TI Visit',
        #     'res_model': 'ec.medical.oi.ti.platform.attempt',
        #     'res_id': oi_ti_platform_attempt.id,
        #     'view_mode': 'form',
        #     'view_id': self.env.ref('ecare_medical_history.view_ec_medical_oi_ti_platform_attempt_form').id,
        #     "target": "new",
        # }

    @api.onchange('tvs_lov', 'tvs_rov', 'tvs_lining_size_decimal', 'tvs_other_text', 'tvs_smooth', 'tvs_distorted', 'tvs_triple_echo',
                  'tvs_hyperechoic_solid', 'tvs_suspected_cavity_lesion', 'tvs_menstruating', 'tvs_cyst_size_ids')
    def _compute_visit_ultrasound_values(self):
        if self:
            for record in self:
                endometrial_character_list = []
                tvs_record = record.ot_ti_visit_tvs_id
                record.oi_ti_follicle_left = str(tvs_record.tvs_lov) if tvs_record.tvs_lov else ''
                record.oi_ti_follicle_right = str(tvs_record.tvs_rov) if tvs_record.tvs_rov else ''
                record.oi_ti_cet = str(tvs_record.tvs_lining_size_decimal) if tvs_record.tvs_lining_size_decimal else ''
                if tvs_record.tvs_smooth:
                    endometrial_character_list.append('Smooth')
                if tvs_record.tvs_distorted:
                    endometrial_character_list.append('Distorted')
                if tvs_record.tvs_triple_echo:
                    endometrial_character_list.append('Triple Echo')
                if tvs_record.tvs_hyperechoic_solid:
                    endometrial_character_list.append('Hyperechoic/Solid')
                if tvs_record.tvs_suspected_cavity_lesion:
                    endometrial_character_list.append('Suspected Cavity Lesion')
                if tvs_record.tvs_menstruating:
                    endometrial_character_list.append('Menstruating')
                if endometrial_character_list:
                    record.oi_ti_endometrial_character = ", ".join(endometrial_character_list)
                else:
                    record.oi_ti_endometrial_character = None
                if tvs_record.tvs_cyst_size_ids:
                    table_rows = []
                    for rec in tvs_record.tvs_cyst_size_ids:
                        type_value = dict(
                            self.env['ec.generic.size']._fields['type'].selection).get(
                            rec.type, '')

                        size_x_value = str(rec.generic_size_x) if rec.generic_size_x is not False else '-'
                        size_y_value = str(rec.generic_size_y) if rec.generic_size_y is not False else '-'
                        table_row = f"<tr><td>{type_value}</td><td>{size_x_value},</td><td></td></tr>"
                        table_rows.append(table_row)
                    dynamic_table = f"<table>{''.join(table_rows)}</table>"
                    record.oi_ti_cyst_computed = dynamic_table
                else:
                    record.oi_ti_cyst_computed = ''

    def _compute_visit_values(self):
        if self:
            for visit in self:
                visit.lmp_date = visit.attempt_cycle_id.repeat_consultation_id.lmp_question_four





