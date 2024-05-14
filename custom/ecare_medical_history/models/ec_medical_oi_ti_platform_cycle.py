from datetime import timedelta

from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalOITIPlatformCycle(models.Model):
    _name = "ec.medical.oi.ti.platform.cycle"
    _description = "OI/TI Platform Cycle/Attempt"
    _order = 'create_date desc'

    oi_ti_platform_attempt_ids = fields.One2many(comodel_name="ec.medical.oi.ti.platform.attempt",
                                                 inverse_name="attempt_cycle_id",
                                                 string="OI/TI Visit")
    oi_ti_platform = fields.Selection(selection=StaticMember.OI_TI_PLATFORM_STATE, string='State',
                                      defult='ready_to_trigger')

    cycle_day = fields.Integer(string='Cycle Day', compute='_compute_cycle_day', store=True)
    oi_ti_schedule = fields.Selection(selection=StaticMember.SCHEDULE,
                                      string='Schedule')
    oi_ti_intervention = fields.Selection(selection=StaticMember.INTERVENTION,
                                          string='Intervention')
    trigger_regimen = fields.Selection(selection=StaticMember.TRIGGER_REGIMEN,
                                       string='Trigger regimen')
    trigger_date_time = fields.Datetime(
        default=fields.datetime.now(),
        string='Trigger date & time')
    second_trigger_regimen = fields.Selection(selection=StaticMember.TRIGGER_REGIMEN,
                                       string='Trigger regimen')
    second_trigger_date_time = fields.Datetime(
        default=fields.datetime.now(),
        string='Trigger date & time')
    indication_of_iui = fields.Selection(selection=StaticMember.INDICATION_OF_IUI,
                                         string='Indication for IUI')
    insemination = fields.Selection(selection=StaticMember.INSEMINATION,
                                    string='Insemination')
    iui_attempt_count = fields.Selection(selection=StaticMember.IUI_ATTEMPT_COUNT,
                                    string='IUI attempt')
    luteal_phase_support = fields.Selection(selection=StaticMember.LUTEAL_PHASE_SUPPORT,
                                            string='Luteal phase support')
    ova_outcome = fields.Selection(selection=StaticMember.OVA_OUTCOME,
                                   string='Outcome')

    #     Inverse Fields
    cycle_timeline_id = fields.Many2one(comodel_name='ec.patient.timeline')
    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation')
    html_table = fields.Html(string='Table', compute='computed_value')
    abandoned_comments = fields.Char(string='Abandoned Comments')

    def _compute_cycle_day(self):
        for record in self:
            if record.repeat_consultation_id.lmp_question_four:
                current_date = fields.Date.today()
                delta = current_date - record.repeat_consultation_id.lmp_question_four
                record.cycle_day = delta.days + 1
            else:
                record.cycle_day = 0

    def create_oi_ti_platform_cycle(self, timeline_id, repeat_consultation_id):
        vals = {
            'cycle_timeline_id': timeline_id.id,
            'repeat_consultation_id': repeat_consultation_id.id,
            'oi_ti_platform': 'ready_to_trigger',
        }
        oi_ti_platform_cycle = self.env['ec.medical.oi.ti.platform.cycle'].create(vals)
        oi_ti_platform_attempt_ref = self.env['ec.medical.oi.ti.platform.attempt']
        oi_ti_platform_attempt_rec = (
            oi_ti_platform_attempt_ref.create_oi_ti_platform_attempt_from_cycle(oi_ti_platform_cycle))
        if oi_ti_platform_attempt_rec:
            oi_ti_platform_cycle.write(
                {
                    'oi_ti_platform_attempt_ids': (0, 0, oi_ti_platform_attempt_rec.id)
                }
            )
        return oi_ti_platform_cycle

    def action_create_oi_ti_platform_attempt(self):
        oi_ti_platform_attempt_ref = self.env['ec.medical.oi.ti.platform.attempt']
        return oi_ti_platform_attempt_ref.create_oi_ti_platform_attempt_from_cycle(self)

    def action_complete_attempt(self):
        if self.insemination is False:
            raise UserError("‘Insemination’ is not entered yet!")
        else:
            self.oi_ti_platform = 'completed'
        # oi_ti_attempts = self.env['ec.medical.oi.ti.platform.attempt'].search([
        #     ('attempt_cycle_id', '=', int(self.id))])
        # attempt_completed = False
        # if oi_ti_attempts:
        #     for rec in oi_ti_attempts:
        #         if rec.oi_ti_attempt_state == 'in_progress':
        #             rec.oi_ti_attempt_state = 'completed'
        #             attempt_completed = True
        #
        #     if attempt_completed is False:
        #         raise UserError("There is no attempt in progress!")

    def action_abandoned_attempt(self):
        if self.insemination is False:
            raise UserError("‘Insemination’ is not entered yet!")
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ec.medical.wizard.note',
                'name': 'Abandon Notes',
                'view_mode': 'form',
                "target": "new",
                "context": {
                    'default_attempt_cycle_id': self.id,
                }
            }
            # self.oi_ti_platform = 'abandoned'
        # oi_ti_attempts = self.env['ec.medical.oi.ti.platform.attempt'].search([
        #     ('attempt_cycle_id', '=', int(self.id))])
        # attempt_completed = False
        # if oi_ti_attempts:
        #     for rec in oi_ti_attempts:
        #         if rec.oi_ti_attempt_state == 'in_progress':
        #             rec.oi_ti_attempt_state = 'abandoned'
        #             attempt_completed = True
        #
        #     if attempt_completed is False:
        #         raise UserError("There is no attempt in progress!")

    def action_2nd_trigger_attempt(self):
        if self.insemination is False:
            raise UserError("‘Insemination’ is not entered yet!")
        else:
            self.oi_ti_platform = '2nd_trigger'

    def action_open_attempt(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ec.medical.oi.ti.platform.cycle',
            'res_id': self.id,
            'name': 'OI/TI Cycle/Attempt',
            'view_mode': 'form',
            "target": "new",
        }

    def action_start_luteal_phase_attempt(self):
        if self.insemination is False:
            raise UserError("‘Insemination’ is not entered yet!")
        else:
            self.oi_ti_platform = 'luteal_phase'

    def get_display_string(self, model_name, field_name, field_value):
        model = self.env[model_name]
        field = model._fields.get(field_name)

        if field and field.type == 'selection':
            return dict(field.selection).get(field_value, field_value)
        else:
            return field_value

    @api.constrains('html_table')
    @api.onchange('oi_ti_platform_attempt_ids')
    def computed_value(self):
        table = ''

        for rec in self:
            table_list = []
            if rec.oi_ti_platform_attempt_ids:
                for attempt in rec.oi_ti_platform_attempt_ids:
                    diagnosis_list = []
                    for diagnosis in attempt.oi_ti_diagnosis_ids:
                        diagnosis_list.append(diagnosis.name) if diagnosis.name else ''
                    diagnosis_name = ', '.join(diagnosis_list)
                    preparation_method_value, oi_ti_attempt_state_value = '', ''
                    if attempt.preparation_method:
                        attempt_model = 'ec.medical.oi.ti.platform.attempt'
                        preparation_method_field = 'preparation_method'
                        preparation_method_value = self.get_display_string(attempt_model, preparation_method_field,
                                                                           attempt.preparation_method)
                    if attempt.oi_ti_attempt_state:
                        attempt_model = 'ec.medical.oi.ti.platform.attempt'
                        oi_ti_attempt_state_field = 'oi_ti_attempt_state'
                        oi_ti_attempt_state_value = self.get_display_string(attempt_model, oi_ti_attempt_state_field,
                                                                            attempt.oi_ti_attempt_state)

                    create_date_formatted = attempt.create_date.strftime("%d-%m-%Y %H:%M")

                    table = (f"<table cellspacing='0' cellpadding='0' class='oi_ti_attempt_table_style'> <tbody> <tr "
                             f"style='height:15.75pt;'> <td colspan='7' class='oi_ti_computed_values_td' "
                             f"style='background-color:#cccccc;'> "
                             f"<p class='oi_ti_text_paragraph_td'>{create_date_formatted or ''}</p> </td> </tr> <tr "
                             f"style='height:15.75pt;'> <td colspan='7' class='oi_ti_attempt_preparation_td' "
                             f"style='background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'><strong><span "
                             f"style='color:#1f1f1f;'> "
                             f"{preparation_method_value or ''}"
                             f"</span></strong></p> </td>"
                           
                             f"</tr> <tr style='height:15.75pt;'> <td "
                             f"class='oi_ti_computed_values_td' style='background-color:#f4cccc;'> <p "
                             f"class='oi_ti_text_paragraph_td'>OI day: 3</p> </td> <td colspan='2' class='oi_ti_heading_td' "
                             f"style='background-color:#fff2cc;'> <p class='oi_ti_action_btn'><strong>LEFT OVARY</strong></p> "
                             f"</td> <td colspan='2' class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                             f"class='oi_ti_action_btn'><strong>RIGHT OVARY</strong></p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#ffffff;'> <p class='oi_ti_action_btn'><strong>Signs of "
                             f"ovulation</strong></p> </td> <td class='oi_ti_attempt_diagnosis_td' "
                             f"style='background-color:#f4cccc;'> <p class='oi_ti_action_btn'><strong>Diagnosis</strong></p> "
                             f"</td> </tr> <tr style='height:26.25pt;'> <td class='oi_ti_computed_values_td' "
                             f"style='background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'>LMP</p> </td> <td "
                             f"class='oi_ti_heading_td' style='background-color:#fff2cc;'> <p "
                             f"class='oi_ti_text_paragraph_td'>Follicle(s)</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#fff2cc;'> <p class='oi_ti_text_paragraph_td'>"
                             f" {attempt.oi_ti_follicle_left or ''}</p> </td> <td "
                             f"class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                             f"class='oi_ti_text_paragraph_td'>Follicle(s)</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#d9ead3;'> <p class='oi_ti_text_paragraph_td'>"
                             f" {attempt.oi_ti_follicle_right or ''} </p> </td> <td "
                             f"class='oi_ti_heading_td' style='background-color:#ffffff;'> <p class='oi_ti_action_btn'>Free "
                             f"fluid, loss of dominant follicle, corpus luteum</p> </td> <td class='oi_ti_attempt_diagnosis_td' "
                             f"style='background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'> "
                             f"{diagnosis_name or ''}"
                             f"<field name='oi_ti_diagnosis_ids'/> "
                             f"</p> </td> </tr> <tr "
                             f"style='height:15.75pt;'> <td class='oi_ti_computed_values_td' style='background-color:#f4cccc;'> "
                             f"<p class='oi_ti_text_paragraph_td'><strong>Cycle day:  "
                             f"{attempt.oi_ti_cycle_day or ''}"
                             f" </strong></p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#fff2cc;'> <p class='oi_ti_text_paragraph_td'><strong>Dominant Follicle("
                             f"s)</strong></p> </td> <td class='oi_ti_heading_td' style='background-color:#fff2cc;'> <p "
                             f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#d9ead3;'> <p class='oi_ti_text_paragraph_td'><strong>Dominant Follicle("
                             f"s)</strong></p> </td> <td class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                             f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#ffffff;'> "
                             f"<p class='oi_ti_text_paragraph_td'>CET: {attempt.oi_ti_cet or ''}</p> </td> <td "
                             f"rowspan='2' class='oi_ti_attempt_diagnosis_td' style='background-color:#f4cccc;'> <p "
                             f"class='oi_ti_text_paragraph_td'>Other diagnoses: "
                             f"{attempt.oi_ti_other_diagnosis or ''}"
                             f"</p> </td> </tr> <tr style='height:26.25pt;'> "
                             f"<td class='oi_ti_computed_values_td' style='background-color:#f4cccc;'> <p "
                             f"class='oi_ti_text_paragraph_td'><strong>AFC (R+L):</strong></p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#fff2cc;'> <p class='oi_ti_text_paragraph_td'>Cyst(s)</p> </td> <td "
                             f"class='oi_ti_heading_td' style='background-color:#fff2cc;'> <p "
                             f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#d9ead3;'> <p class='oi_ti_text_paragraph_td'>Cyst(s)</p> </td> <td "
                             f"class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                             f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                             f"style='background-color:#ffffff;'> <p class='oi_ti_text_paragraph_td'>Endometrial character: "
                             f"smooth, triple echo</p> </td> </tr> <tr style='height:15.75pt;'> <td colspan='7' "
                             f"style='border-top:0.75pt solid #cccccc; padding:2pt 1.62pt; vertical-align:top; "
                             f"background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'>"
                             f"Comments: {attempt.oi_ti_comments or ''}</p> </td> </tr> </tbody> "
                             f"</table>")
                    table_list.append(table)

                rec.html_table = ''.join(table_list)
            else:
                rec.html_table = None
                
    def write(self, vals):
        if self.oi_ti_platform == 'completed' or self.oi_ti_platform == 'abandoned':
            raise UserError(f"You can't change Completed/Abandoned attempt, please create a new one!")
        else:
            return super(EcMedicalOITIPlatformCycle, self).write(vals)


class EcMedicalNotes(models.TransientModel):
    _name = "ec.medical.wizard.note"
    _description = "Wizard for adding new notes at the time of action"
    
    attempt_cycle_id = fields.Many2one(comodel_name='ec.medical.oi.ti.platform.cycle',
                                       readonly=True,
                                       ondelete="restrict")
    note = fields.Text('Comments')
    
    @api.model
    def create(self, vals):
        res = super(EcMedicalNotes, self).create(vals)
        if res:
            res.attempt_cycle_id.abandoned_comments = res.note
            res.attempt_cycle_id.oi_ti_platform = 'abandoned'
        return res
