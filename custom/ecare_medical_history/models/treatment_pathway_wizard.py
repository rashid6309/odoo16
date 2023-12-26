from odoo import models, fields, api


class TreatmentPathwayWizard(models.TransientModel):
    _name = 'ec.medical.treatment.pathway.wizard'
    _description = "Treatment Pathway Wizard"

    message = fields.Text('Message')

