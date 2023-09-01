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
