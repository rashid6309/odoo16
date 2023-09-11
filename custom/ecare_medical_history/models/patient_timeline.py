import uuid

from odoo import models, fields

from odoo import http
from odoo.http import request

class PatientTimeline(models.Model):
    _name = "ec.patient.timeline"
    _description = "Patient Timeline"

    name = fields.Char(string="Name")
    patient_id = fields.Many2one(comodel_name="ec.medical.patient")

    def action_open_patient_time_view(self):
        request.session['patient_id'] = str(self.patient_id.id)
        return self.env['ec.first.consultation'].action_open_patient_first_consultation(self.patient_id.id)
