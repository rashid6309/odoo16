
from odoo import http
from odoo.http import request


class EcMedicalHistoryController(http.Controller):

    @http.route('/banner/generic_patient_summery_detailed', auth='user', type='json')
    def generic_patient_summery(self):
        """ Returns the `banner` for the account dashboard onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """
        # selected_patient_id = request.env['ir.config_parameter'].sudo().get_param('selected_patient_id')
        # environment = http.request.env

        patient_id = self.get_patient()

        return {
            'html': request.env['ir.qweb']._render('ecare_medical_history.patient_summery', {
                'patient_id': patient_id or None
            })
        }

    def get_patient(self):
        patient_id = None
        if request.params:

            model_id = request.params['model_id']
            record_id = request.params['record_id']
            if model_id == 'ec.medical.patient':
                record = request.env[model_id].browse([int(record_id)])
                if record:
                    patient_id = record
            else:
                record = request.env[model_id].browse([int(record_id)])
                if record:
                    patient_id = record.patient_id
        return patient_id
