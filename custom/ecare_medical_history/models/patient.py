from odoo import models, fields, _
from odoo.exceptions import ValidationError

''' Not required Specify reason  

    *. This is not required now as we are navigating it from the patient.timeline now.
    
'''


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
