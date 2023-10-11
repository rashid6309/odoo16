from odoo import models, fields, api, _


class PatientTimelineWizard(models.TransientModel):
    _name = "ec.patient.timeline.wizard"
    _description = "Wizard to select patient"

    patient = fields.Many2one('ec.medical.patient', required=1)

    def create_timeline(self):
        patient_timeline_obj = self.env['ec.patient.timeline']
        timeline_values = patient_timeline_obj.action_mandatory_patient_timeline(self.patient)
        if timeline_values:
            timeline = patient_timeline_obj.create(timeline_values)
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'ec.patient.timeline',
                'res_id': timeline.id,
                'name': timeline.timeline_patient_name,
                'view_mode': 'form',
                "target": "current",
            }
