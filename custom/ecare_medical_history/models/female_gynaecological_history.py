from datetime import date, datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class FemaleGynaecologicalHistory(models.Model):
    _name = 'ec.medical.gynaecological.history'
    _description = "Female Gynaecological History"

    MENARCHE_TYPE = [('irregular_since_menarche', 'Irregular Since Menarche'),
                     ]
    MENARCHE_CYCLE = [
        ('regular', 'Regular'),
        ('irregular', 'Irregular'),
        ('comments', 'Comments'),
    ]

    MENSTRUAL_FLOW = [
        ('normal', 'Normal'),
        ('scanty', 'Scanty'),
        ('excessive', 'Excessive'),
    ]

    DYSMENORRHOEA = [
        ('before_menses', 'Before Menses'),
        ('during_menses', 'During Menses'),
        ('after_menses', 'After Menses'),
        ('none', 'None'),
    ]    
    
    INTENSITY = [
        ('increase', 'Increase'),
        ('decrease', 'Decrease'),
        ('none', 'None'),
    ]

    female_age_at_menarche = fields.Char(string='Age at Menarche')
    female_menarche_type = fields.Selection(selection=MENARCHE_TYPE, string='Age at Menarche')
    female_menstrual_cycle = fields.Selection(selection=MENARCHE_CYCLE, string='Menstrual Cycle')
    female_menstrual_days = fields.Date(string='Menstrual Cycle')
    female_menstrual_gap = fields.Date(string='Menstrual Cycle')
    female_menstrual_comments = fields.Date(string='Menstrual Cycle')
    female_menstrual_days_from = fields.Date(string='Menstrual Cycle')
    female_menstrual_days_to = fields.Date(string='Menstrual Cycle')
    female_menstrual_all_comments = fields.Date(string='Menstrual Cycle')
    female_menstrual_flow = fields.Selection(selection=MENSTRUAL_FLOW, string='Menstrual Flow')
    female_dysmenorrhoea = fields.Selection(selection=DYSMENORRHOEA, string='Dysmenorrhoea')
    female_pain_intensity = fields.Selection(selection=INTENSITY, string='Pain Intensity')
    female_lmp = fields.Date(string='LMP')
    female_complications = fields.Char(string='Complications')
    female_complications_other = fields.Char(string='Complications')
    female_complains = fields.Char(string='Complains')

