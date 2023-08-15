from odoo import models, fields


class FirstConsultation(models.Model):
    _name = 'ec.medical.first.consultation'
    _description = "First Consultation"

    _inherit = ['ec.medical.general.examination', 'ec.medical.obstetrics.history', 'ec.medical.gynaecological.history']

    name = fields.Char(string='Name')

    obs_history_ids = fields.One2many('ec.medical.obstetrics.history', 'consultation_id', string='Obstetrics History')



