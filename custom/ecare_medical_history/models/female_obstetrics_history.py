from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_core.utilities.helper import TimeValidation
from odoo.addons.ecare_core.utilities.time_conversion import CustomDateTime
'''

TODO: Review attributes name
REVIEW FULL FILE

'''

class FemaleObstetricsHistory(models.Model):
    _name = 'ec.obstetrics.history'
    _description = "Female Obstetrics History"
    _order = "create_date desc"

    patient_id = fields.Many2one(comodel_name='ec.medical.patient', string='Patient') # Why it is required??
    timeline_id = fields.Many2one(comodel_name='ec.patient.timeline', string='Patient Timeline')

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

    gender = fields.Selection(string='Child Gender', selection=StaticMember.GENDER)
    weight = fields.Selection(string='Child Weight', selection=StaticMember.WEIGHT)
    health = fields.Selection(string='Child Health', selection=StaticMember.HEALTH)
    alive = fields.Selection(string='Child Alive', selection=StaticMember.ALIVE)
    feed = fields.Selection(string='Child Feed', selection=StaticMember.FEED)
    state = fields.Boolean(string='', default=True)

    labour_history = fields.Selection(selection=StaticMember.LABOUR_HISTORY,
                                      string='Labour')
    # legacy_system_ID = fields.Char(string='Legacy System Id')

    ''' Constrains '''
    @api.constrains('date_of_birth')
    def _check_dob_date(self):
        for record in self:
            if CustomDateTime.greater_than_today(record.date_of_birth):
                raise ValidationError(_(
                    "Date of Birth can't be greater than current date!"))
    @api.depends('date_of_birth')
    def _get_age(self):
        for rec in self:
            rec.age = TimeValidation.convert_date_to_days_years(rec.date_of_birth)


    ''' Constrains block ended '''

    def action_open_form_view(self, patient_id, timeline_id=None):
        context = {
            'default_patient_id': patient_id.id,
            'default_timeline_id': timeline_id.id if timeline_id else None,
        }

        domain = ['|',
                  ('timeline_id', '=', timeline_id.id if timeline_id else None),
                  ('patient_id', '=', patient_id.id)
                  ]
        return {
            "name": _("Patient Obstetrics History"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.obstetrics.history',
            'view_id': self.env.ref('ecare_medical_history.ec_medical_obstetrics_history_tree_view').id,
            'view_mode': 'tree',
            "target": 'new',
            'context': context,
            'flags': {'initial_mode': 'create'},
            'domain': domain,
        }
