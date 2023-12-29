from odoo import models, fields, api


class TreatmentPathwayWizard(models.TransientModel):
    _name = 'ec.medical.treatment.pathway.wizard'
    _description = "Treatment Pathway Wizard"

    message = fields.Text('Message')
    ec_repeat_consultation_id = fields.Many2one('ec.repeat.consultation')

    def action_understand_wizard(self):
        if self.ec_repeat_consultation_id:
            return self.ec_repeat_consultation_id.action_state_to_decision_pending()

