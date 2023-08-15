from odoo import models, fields


class FirstConsultation(models.Model):
    _name = 'ec.medical.first.consultation'
    _description = "Patient First Consultation"
    _inherits = {'ec.medical.general.examination': 'medical_general_examination_id',
                 'ec.medical.obstetrics.history': 'medical_obstetrics_history_id',
                 'ec.medical.gynaecological.history': 'medical_gynaecological_history_id'
                }

    # Inherits synchronized objects.
    medical_general_examination_id = fields.Many2one(comodel_name="ec.medical.general.examination")
    medical_obstetrics_history_id = fields.Many2one(comodel_name="ec.medical.obstetrics.history")
    medical_gynaecological_history_id = fields.Many2one(comodel_name="ec.medical.gynaecological.history")

    # Normal Attributes
    name = fields.Char(string='Name')


    patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                 required=True)

    obs_history_ids = fields.One2many(comodel_name='ec.medical.obstetrics.history',
                                      inverse_name='consultation_id',
                                      string='Obstetrics History')
