from datetime import date, datetime

from odoo import api, models, fields, _
from odoo.exceptions import UserError, ValidationError


class FemaleObstetricsHistory(models.Model):
    _name = 'ec.medical.obstetrics.history'
    _description = "Female Obstetrics History"

    patient = fields.Many2one(comodel_name='ec.medical.patient', string='Patient')
    consultation_id = fields.Many2one(comodel_name='ec.medical.first.consultation', string='First Consultation')

    # infant_id = fields.Many2one('ec.medical.obs.labr.infants', ondelete='cascade')

    DoP = [('<6', '<6'),
           ('6', '6'),
           ('7', '7'),
           ('8', '8'),
           ('9', '9'),
           ('10', '10'),
           ('11', '11'),
           ('12', '12'), ('13', '13'),
           ('14', '14'), ('15', '15'),
           ('16', '16'), ('17', '17'),
           ('18', '18'), ('19', '19'),
           ('20', '20'), ('21', '21'),
           ('22', '22'), ('23', '23'),
           ('24', '24'),
           ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'),
           ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'),
           ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'),
           ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'),
           ('>40', '>40'),
           ]

    # MoD = [('Ectopic', 'ECTOPIC'),
    #        ('CAESAREAN', 'CAESAREAN'),
    #        ('FORCEPS', 'FORCEPS'),
    #        ('MISCARRIAGE', 'MISCARRIAGE'),
    #        ('SVD', 'SVD'),
    #        ('TOP', 'TOP'),
    #        ('VENTOUSE', 'VENTOUSE'), ]

    MoD = [('ABORTION', 'ABORTION'),
           ('SVD', 'SVD'),
           ('VENTOUSE', 'VENTOUSE'),
           ('FORCEPS', 'FORCEPS'),
           ('CAESAREAN', 'CAESAREAN'),
           ('MISCARRIAGE', 'MISCARRIAGE'),
           ('TOP', 'TOP'),
           ('Ectopic', 'ECTOPIC'),
           ('VBAC', 'VBAC'), ]
    GENDER = [('Male', 'Male'), ('Female', 'Female'), ('Ambiguous', 'Ambiguous'), ('N/A', 'N/A'), ]
    WEIGHT = [('<500', '<500 gms'),
              ('500', '500 gms'),
              ('600', '600 gms'),
              ('700', '700 gms'),
              ('800', '800 gms'),
              ('900', '900 gms'),
              ('1000', '1000 gms'),
              ('1100', '1100 gms'),
              ('1200', '1200 gms'),
              ('1300', '1300 gms'),
              ('1400', '1400 gms'),
              ('1500', '1500 gms'),
              ('1600', '1600 gms'),
              ('1700', '1700 gms'),
              ('1800', '1800 gms'),
              ('1900', '1900 gms'),
              ('2000', '2000 gms'),
              ('2100', '2100 gms'),
              ('2200', '2200 gms'),
              ('2300', '2300 gms'),
              ('2400', '2400 gms'),
              ('2500', '2500 gms'),
              ('2600', '2600 gms'),
              ('2700', '2700 gms'),
              ('2800', '2800 gms'),
              ('2900', '2900 gms'),
              ('3000', '3000 gms'),
              ('3100', '3100 gms'),
              ('3200', '3200 gms'),
              ('3300', '3300 gms'),
              ('3400', '3400 gms'),
              ('3500', '3500 gms'),
              ('3600', '3600 gms'),
              ('3700', '3700 gms'),
              ('3800', '3800 gms'),
              ('3900', '3900 gms'),
              ('4000', '4000 gms'),
              ('4100', '4100 gms'),
              ('4200', '4200 gms'),
              ('4300', '4300 gms'),
              ('4400', '4400 gms'),
              ('4500', '4500 gms'),
              ('4600', '4600 gms'),
              ('4700', '4700 gms'),
              ('4800', '4800 gms'),
              ('>4800', '>4800 gms'),

              ]

    HEALTH = [('N/A', 'N/A'),
              ('Alive', 'Alive'),
              ('nnd3d', 'NND in 3 days'),
              ('nnd7d', 'NND in 7 days'),
              ('nnd10d', 'NND in 10 days'),
              ('id6m', 'Infant death within 6 months'),
              ('cd6m1y', 'Child death 6 months to 1 year'),
              ('cd1y', 'Child death after 1 year'),
              ('NND-28', 'NND-28'),
              ('Died within 1 year', 'Died within 1 year'),
              ('Died within 1 month', 'Died within 1 month'),
              ]
    ALIVE = [('N/A', 'N/A'), ('Alive', 'Alive'), ('SB', 'SB'), ]
    FEED = [('Mother', 'Mother'), ('Artificial', 'Artificial'), ('N/A', 'N/A'), ]

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

    baby_name = fields.Char(string='Baby Name')
    pob = fields.Char(string="Birth Place",
                      required=False, )
    dob = fields.Date(string='Date of Birth')
    age = fields.Char(string='Age', compute='_get_age')
    baby_notes = fields.Text(string='Baby Notes')
    dop = fields.Selection(string='Duration of Pregnancy', selection=DoP)
    mod = fields.Selection(string='Mode Of delivery', selection=MoD)
    # indication = fields.Many2many('ec.medical.obs.labr.indi',
    #                               relation='obstetrics_hx_indication_rel', column1='obs_hx',
    #                               column2='lab_indi', string='Indication of Caesarean')
    other_indications = fields.Char('Other Indications')
    complications = fields.Text(string='Complications in Pregnancy')
    comp_del = fields.Text(string='Complications in Delivery')
    comp_pp = fields.Text(string='Complications in Post-partum')
    comp_prag = fields.Text(string='Complication In Pregnancy')
    gender = fields.Selection(string='Gender', selection=GENDER)
    weight = fields.Selection(string='Weight', selection=WEIGHT)
    health = fields.Selection(string='Health', selection=HEALTH)
    alive = fields.Selection(string='Alive', selection=ALIVE)
    feed = fields.Selection(string='Feed', selection=FEED)
    state = fields.Boolean(string='', default=True)
    labour_history = fields.Selection([('spontaneous', 'Spontaneous'),
                                       ('induced', 'Induced'),
                                       ], string='Labour')
    legacy_system_ID = fields.Char('Legacy System Id', force_save=True)

    def name_get(self):
        return [(self.id, 'Obstetrics History')]

    @api.constrains('dob', )
    @api.onchange('dob')
    def _check_dob_date(self):
        for record in self:
            if record.dob and record.dob > fields.Date.today():
                raise ValidationError(_(
                    "Date of Birth can't be greater than current date!"))