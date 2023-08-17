from odoo import models, fields


class FirstConsultation(models.Model):
    _name = 'ec.first.consultation'
    _description = "Patient First Consultation"

    _inherits = {'ec.general.history': 'ec_general_examination_id',
                 'ec.obstetrics.history': 'ec_obstetrics_history_id',
                 'ec.gynaecological.history': 'ec_gynaecological_history_id'
                }

    # Inherits synchronized objects.
    ec_general_examination_id = fields.Many2one(comodel_name="ec.general.history")
    ec_obstetrics_history_id = fields.Many2one(comodel_name="ec.obstetrics.history")
    ec_gynaecological_history_id = fields.Many2one(comodel_name="ec.gynaecological.history")
    ec_social_history_id = fields.Many2one(comodel_name="ec.social.history")

    # Normal Attributes
    name = fields.Char(string='Name')


    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 required=True)

    obs_history_ids = fields.One2many(comodel_name='ec.obstetrics.history',
                                      inverse_name='consultation_id',
                                      string='Obstetrics History')
