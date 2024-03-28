from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleGynaecologicalHistory(models.Model):
    _name = 'ec.gynaecological.history'
    _description = "Female Gynecological History"

    gynaecological_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                                ondelete='restrict')

    female_age_at_menarche = fields.Selection(selection=StaticMember.AGE_AT_MENARCHE, string='Age at Menarche')
    female_menarche_type = fields.Selection(selection=StaticMember.MENARCHE_TYPE, string='Age at Menarche')
    female_menstrual_cycle = fields.Selection(selection=StaticMember.MENARCHE_CYCLE, string='Menstrual Cycle')
    female_menstrual_days = fields.Selection(selection=StaticMember.MENARCHE_CYCLE_DAYS, string='Menstrual Cycle Days')
    female_menstrual_gap = fields.Selection(selection=StaticMember.MENARCHE_CYCLE_DAYS, string='Menstrual Cycle Gap')
    female_menstrual_comments = fields.Char(string='Menstrual Cycle Comments')
    female_menstrual_days_from = fields.Selection(selection=StaticMember.MENARCHE_CYCLE_DAYS, string='Menstrual Cycle Days From')
    female_menstrual_days_to = fields.Selection(selection=StaticMember.MENARCHE_CYCLE_DAYS, string='Menstrual Cycle Days to')

    female_menstrual_gap_from = fields.Selection(selection=StaticMember.MENARCHE_CYCLE_DAYS, string='Menstrual Cycle Gap From')
    female_menstrual_gap_to_month = fields.Selection(selection=StaticMember.MENSTRUAL_CYCLE_TO, string='Menstrual Cycle Gap to')
    female_menstrual_gap_other = fields.Char(string='Menstrual Cycle Gap Other')
    female_menstrual_all_comments = fields.Char(string='Menstrual Cycle All Comments')
    female_menstrual_flow = fields.Selection(selection=StaticMember.MENSTRUAL_FLOW, string='Menstrual Flow')
    female_dysmenorrhoea_check = fields.Boolean('Dysmenorrhoea')
    female_dysmenorrhoea_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                relation='gynaecological_history_multi_selection_dysmenorrhoea',
                                                column1='gynaecological_id',
                                                column2='multi_selection_id',
                                                string='Dysmenorrhoea', domain="[('type', '=', 'dysmenorrhoea')]")
    female_pain_intensity = fields.Selection(selection=StaticMember.INTENSITY, string='Pain Intensity')
    female_lmp = fields.Date(string='LMP')
    female_complications_check = fields.Boolean('Complications')
    female_complications_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                relation='gynaecological_history_multi_selection_complications',
                                                column1='gynaecological_id',
                                                column2='multi_selection_id',
                                                string='Complications', domain="[('type', '=', 'complications')]")

    female_complications_other = fields.Char(string='Other Complications')
    female_complains_check = fields.Boolean('Complains')
    female_complains_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                            relation='gynaecological_history_multi_selection_complains',
                                            column1='gynaecological_id',
                                            column2='multi_selection_id',
                                            string='Complaints', domain="[('type', '=', 'complains')]")


