from odoo import models, fields, api, _


class PatientTimelineWizard(models.TransientModel):
    _name = "ec.patient.timeline.wizard"
    _description = "Wizard to select patient"

    patient = fields.Many2one('ec.medical.patient', required=1)

    def create_timeline(self):
        patient_timeline_id = self.env['ec.patient.timeline'].action_create_timeline_from_patient(self.patient)
        if patient_timeline_id:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ec.patient.timeline',
                'res_id': patient_timeline_id.id,
                'name': patient_timeline_id.timeline_patient_name,
                'view_mode': 'form',
                "target": "current",
            }
