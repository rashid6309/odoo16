from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_core.utilities.helper import TimeValidation

from datetime import date, datetime
'''

TODO: Review attributes name
REVIEW FULL FILE

'''

class FemaleObstetricsHistory(models.Model):
    _name = 'ec.obstetrics.history'
    _description = "Female Obstetrics History"

    patient_id = fields.Many2one(comodel_name='ec.medical.patient', string='Patient') # Why it is required??
    first_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', string='First Consultation')

    @api.depends('date_of_birth')
    def _get_age(self):
        for rec in self:
            rec.date_of_birth = TimeValidation.convert_date_to_days_years(rec.date_of_birth)

    baby_name = fields.Char(string='Baby Name')
    birth_place = fields.Char(string="Birth Place",
                      required=False, )
    date_of_birth = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_get_age')
    baby_notes = fields.Text(string='Baby Notes')
    duration_of_pregnancy = fields.Selection(string='Duration of Pregnancy', selection=StaticMember.DoP)
    mode_of_delivery = fields.Selection(string='Mode Of delivery', selection=StaticMember.MoD)
    other_indications = fields.Char('Other Indications')
    complications = fields.Text(string='Complications in Pregnancy')
    complication_delivery = fields.Text(string='Complications in Delivery')

    complication_post_partum = fields.Text(string='Complications in Post-partum')
    complication_pregnancy = fields.Text(string='Complication In Pregnancy')

    gender = fields.Selection(string='Gender', selection=StaticMember.GENDER)
    weight = fields.Selection(string='Weight', selection=StaticMember.WEIGHT)
    health = fields.Selection(string='Health', selection=StaticMember.HEALTH)
    alive = fields.Selection(string='Alive', selection=StaticMember.ALIVE)
    feed = fields.Selection(string='Feed', selection=StaticMember.FEED)
    state = fields.Boolean(string='', default=True)
    '''
    TODO: MOVE to Static
    '''
    labour_history = fields.Selection([('spontaneous', 'Spontaneous'),
                                       ('induced', 'Induced'),
                                       ], string='Labour')
    legacy_system_ID = fields.Char(string='Legacy System Id')

    # @api.constrains('dob', )
    # def _check_dob_date(self):
    #     for record in self:
    #         if record.dob and record.dob > fields.Date.today():
    #             raise ValidationError(_(
    #                 "Date of Birth can't be greater than current date!"))