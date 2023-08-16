from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class FemaleGynaecologicalHistory(models.Model):
    _name = 'ec.gynaecological.history'
    _description = "Female Gynaecological History"

    female_age_at_menarche = fields.Char(string='Age at Menarche')
    female_menarche_type = fields.Selection(selection=StaticMember.MENARCHE_TYPE, string='Age at Menarche')
    female_menstrual_cycle = fields.Selection(selection=StaticMember.MENARCHE_CYCLE, string='Menstrual Cycle')
    female_menstrual_days = fields.Date(string='Menstrual Cycle')
    female_menstrual_gap = fields.Date(string='Menstrual Cycle')
    female_menstrual_comments = fields.Date(string='Menstrual Cycle')
    female_menstrual_days_from = fields.Date(string='Menstrual Cycle')
    female_menstrual_days_to = fields.Date(string='Menstrual Cycle')
    female_menstrual_all_comments = fields.Date(string='Menstrual Cycle')
    female_menstrual_flow = fields.Selection(selection=StaticMember.MENSTRUAL_FLOW, string='Menstrual Flow')
    female_dysmenorrhoea = fields.Selection(selection=StaticMember.DYSMENORRHOEA, string='Dysmenorrhoea')
    female_pain_intensity = fields.Selection(selection=StaticMember.INTENSITY, string='Pain Intensity')
    female_lmp = fields.Date(string='LMP')
    female_complications = fields.Char(string='Complications')
    female_complications_other = fields.Char(string='Complications')
    female_complains = fields.Char(string='Complains')

