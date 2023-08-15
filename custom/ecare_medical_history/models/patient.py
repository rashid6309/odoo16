from odoo import models, fields, _
from odoo.exceptions import ValidationError

class EcMedicalPatient(models.Model):
    _inherit = "ec.medical.patient"


    ''' Overriden methods '''

    def action_register(self):
        try:
            super().action_register()
            self.env['ec.individual.patient'].create_individuals(self.id)
        except Exception:
            raise ValidationError("Action Register is failing. Please contact administrator.")

        return True

    ''' XXX -- END -- XXX '''


    def action_open_patient_first_consultation(self):
        first_consultation_id = self.env['ec.medical.first.consultation'].search(domain=[('patient_id', '=', self.id)])

        value = {}
        if first_consultation_id:
            value = {'res_id': first_consultation_id.id}

        context = self.env.context.copy()

        context.update({
            'default_patient_id': self.id,
        })
        action = {
            "name": _("First Consultation"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.medical.first.consultation',
            'view_mode': 'form',
            'view_id': self.env.ref('ecare_medical_history.ec_medical_first_consultation_form_view').id,
            "context": context,
            "target": 'current',
        }

        action.update(value)
        return action
