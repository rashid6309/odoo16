from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember

from datetime import date, datetime


class FemaleObstetricsHistory(models.Model):
    _name = 'ec.obstetrics.history'
    _description = "Female Obstetrics History"

    patient = fields.Many2one(comodel_name='ec.medical.patient', string='Patient') # Why it is required??
    consultation_id = fields.Many2one(comodel_name='ec.first.consultation', string='First Consultation')

    @api.depends('dob')
    @api.onchange('dob')
    def _get_age(self):
        for r in self:
            if r.dob:
                bdate = datetime.strptime(str(r.dob), "%Y-%m-%d").date()
                today = date.today()
                # if bdate > today:
                #     r.dob = today
                #     raise ValidationError('Date of Birth should be lesser than or equal to today')
                diffdate = today - bdate
                years = diffdate.days / 365
                formonth = diffdate.days - (int(years) * 365.25)
                months = (formonth / 31)
                bday = bdate.day
                tody = date.today().day
                if tody >= bday:
                    day = tody - bday
                else:
                    day = 31 - (bday - tody)
                if int(years) < 5:

                    r.age = str(int(years)) + 'Y ' + str(int(months)) + 'M ' + str(day) + 'D'
                else:
                    r.age = str(int(years)) + ' Years'
            else:
                r.age = None

    baby_name = fields.Char(string='Baby Name')
    pob = fields.Char(string="Birth Place",
                      required=False, )
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_get_age')
    baby_notes = fields.Text(string='Baby Notes')
    dop = fields.Selection(string='Duration of Pregnancy', selection=StaticMember.DoP)
    mod = fields.Selection(string='Mode Of delivery', selection=StaticMember.MoD)
    # indication = fields.Many2many('ec.medical.obs.labr.indi',
    #                               relation='obstetrics_hx_indication_rel', column1='obs_hx',
    #                               column2='lab_indi', string='Indication of Caesarean')
    other_indications = fields.Char('Other Indications')
    complications = fields.Text(string='Complications in Pregnancy')
    comp_del = fields.Text(string='Complications in Delivery')
    comp_pp = fields.Text(string='Complications in Post-partum')
    comp_prag = fields.Text(string='Complication In Pregnancy')
    gender = fields.Selection(string='Gender', selection=StaticMember.GENDER)
    weight = fields.Selection(string='Weight', selection=StaticMember.WEIGHT)
    health = fields.Selection(string='Health', selection=StaticMember.HEALTH)
    alive = fields.Selection(string='Alive', selection=StaticMember.ALIVE)
    feed = fields.Selection(string='Feed', selection=StaticMember.FEED)
    state = fields.Boolean(string='', default=True)
    labour_history = fields.Selection([('spontaneous', 'Spontaneous'),
                                       ('induced', 'Induced'),
                                       ], string='Labour')
    legacy_system_ID = fields.Char('Legacy System Id', force_save=True)

    # @api.constrains('dob', )
    # def _check_dob_date(self):
    #     for record in self:
    #         if record.dob and record.dob > fields.Date.today():
    #             raise ValidationError(_(
    #                 "Date of Birth can't be greater than current date!"))