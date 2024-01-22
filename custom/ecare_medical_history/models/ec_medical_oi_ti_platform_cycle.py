from odoo import models, api, fields
from odoo.exceptions import UserError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalOITIPlatformCycle(models.Model):
    _name = "ec.medical.oi.ti.platform.cycle"
    _description = "OI/TI Platform Cycle"
    _order = 'create_date desc'

    oi_ti_platform_attempt_ids = fields.One2many(comodel_name="ec.medical.oi.ti.platform.attempt",
                                                 inverse_name="attempt_cycle_id",
                                                 string="OI/TI Platform Attempt")

    cycle_day = fields.Integer(string='Cycle Day', compute='_compute_cycle_day', store=True)
    trigger_regimen = fields.Selection(selection=StaticMember.TRIGGER_REGIMEN,
                                       string='Trigger regimen')
    trigger_date_time = fields.Datetime(
        default=fields.datetime.now(),
        string='Trigger date & time')
    indication_of_iui = fields.Selection(selection=StaticMember.INDICATION_OF_IUI,
                                         string='Indication for IUI')
    insemination = fields.Selection(selection=StaticMember.INSEMINATION,
                                    string='Insemination')
    luteal_phase_support = fields.Selection(selection=StaticMember.LUTEAL_PHASE_SUPPORT,
                                            string='Luteal phase support')

    #     Inverse Fields
    cycle_timeline_id = fields.Many2one(comodel_name='ec.patient.timeline')
    repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation')
    html_table = fields.Html(string='Table', compute='computed_value')

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
        oi_ti_attempts = self.env['ec.medical.oi.ti.platform.attempt'].search([
            ('attempt_cycle_id', '=', int(self.id))])
        attempt_completed = False
        if oi_ti_attempts:
            for rec in oi_ti_attempts:
                if rec.oi_ti_attempt_state == 'in_progress':
                    rec.oi_ti_attempt_state = 'completed'
                    attempt_completed = True

            if attempt_completed is False:
                raise UserError("There is no attempt in progress!")

    @api.constrains('html_table')
    def computed_value(self):
        table = ''
        for rec in self:
            for attempt in rec.oi_ti_platform_attempt_ids:
                table = (f"<table cellspacing='0' cellpadding='0' class='oi_ti_attempt_table_style'> <tbody> <tr "
                         f"style='height:15.75pt;'> <td colspan='7' class='oi_ti_computed_values_td' "
                         f"style='background-color:#cccccc;'> <p class='oi_ti_text_paragraph_td'/> </td> </tr> <tr "
                         f"style='height:15.75pt;'> <td colspan='7' class='oi_ti_attempt_preparation_td' "
                         f"style='background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'><strong><span "
                         f"style='color:#1f1f1f;'> "
                         f"{attempt.preparation_method}"
                         f"</span></strong></p> </td> </tr> <tr style='height:15.75pt;'> <td "
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
                         f"( {attempt.oi_ti_follicle_left})</p> </td> <td "
                         f"class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                         f"class='oi_ti_text_paragraph_td'>Follicle(s)</p> </td> <td class='oi_ti_heading_td' "
                         f"style='background-color:#d9ead3;'> <p class='oi_ti_text_paragraph_td'>"
                         f"( {attempt.oi_ti_follicle_right} )</p> </td> <td "
                         f"class='oi_ti_heading_td' style='background-color:#ffffff;'> <p class='oi_ti_action_btn'>Free "
                         f"fluid, loss of dominant follicle, corpus luteum</p> </td> <td class='oi_ti_attempt_diagnosis_td' "
                         f"style='background-color:#f4cccc;'> <p class='oi_ti_text_paragraph_td'> "
                         f"{attempt.oi_ti_diagnosis_ids.name}"
                         # f"<field name='oi_ti_diagnosis_ids'/> "
                         f"</p> </td> </tr> <tr "
                         f"style='height:15.75pt;'> <td class='oi_ti_computed_values_td' style='background-color:#f4cccc;'> "
                         f"<p class='oi_ti_text_paragraph_td'><strong>Cycle day:  "
                         f"{attempt.oi_ti_cycle_day}"
                         f" </strong></p> </td> <td class='oi_ti_heading_td' "
                         f"style='background-color:#fff2cc;'> <p class='oi_ti_text_paragraph_td'><strong>Dominant Follicle("
                         f"s)</strong></p> </td> <td class='oi_ti_heading_td' style='background-color:#fff2cc;'> <p "
                         f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                         f"style='background-color:#d9ead3;'> <p class='oi_ti_text_paragraph_td'><strong>Dominant Follicle("
                         f"s)</strong></p> </td> <td class='oi_ti_heading_td' style='background-color:#d9ead3;'> <p "
                         f"class='oi_ti_text_paragraph_td'>None</p> </td> <td class='oi_ti_heading_td' "
                         f"style='background-color:#ffffff;'> <p class='oi_ti_text_paragraph_td'>CET: 11</p> </td> <td "
                         f"rowspan='2' class='oi_ti_attempt_diagnosis_td' style='background-color:#f4cccc;'> <p "
                         f"class='oi_ti_text_paragraph_td'>Other diagnoses: "
                         f"{attempt.oi_ti_other_diagnosis}"
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
                         f"Comments: {attempt.oi_ti_comments}</p> </td> </tr> </tbody> "
                         f"</table>")

            rec.html_table = table
