from odoo import models, fields, api


class PatientTimeline(models.Model):
    _name = "ec.patient.timeline"
    _description = "Patient Timeline"
    _rec_name = "timeline_patient_id"
    _inherits = {'ec.first.consultation': 'ec_first_consultation_id'}


    timeline_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                          string="Patient",
                                          index=True)

    ec_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete='restrict')

    ''' 
    * Anywhere banner is required we can use this. 
    * No other purpose of this its just
    * Conceptually we can use the widget on anyfield. 
    '''

    @api.onchange("timeline_patient_id")
    def populate_dependent_patient_field(self):
        """
            We are only updating the first_consultation, and in the hind case, it'll trigger all other patients
        """
        for record in self:
            patient_id = record.timeline_patient_id
            record.first_consultation_patient_id = patient_id
            record.ec_first_consultation_id.populate_all_patients()
            # record.first_consultation_patient_id.populate_all_patients()

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
