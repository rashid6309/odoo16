from odoo import models, fields, api


class PatientTimeline(models.Model):
    _name = "ec.patient.timeline"
    _description = "Patient Timeline"
    _inherits = {'ec.first.consultation': 'ec_first_consultation_id'}

    name = fields.Char(string="Name")
    timeline_patient_id = fields.Many2one(comodel_name="ec.medical.patient", index=True)

    ec_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete='restrict')

    ''' FIX: Rename to this meaningful.'''
    test_field = fields.Char('trip_summary')

    @api.onchange("timeline_patient_id")
    def populate_dependent_patient_field(self):
        for record in self:
            record.patient_id = self.timeline_patient_id

    def action_open_patient_time_view(self):
        patient_id = self.env.context.get('0')
        return {
            'name': 'Patient',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'ec.medical.patient',
            'res_id': patient_id,
            'target': 'new',
        }
