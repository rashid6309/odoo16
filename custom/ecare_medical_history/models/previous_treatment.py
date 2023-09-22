from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcMedicalPreviousHistory(models.Model):
    _name = 'ec.medical.previous.treatment'
    _description = "Previous Treatment"

    first_consultation_id = fields.Many2one('ec.first.consultation', string='First Consultation')
    type = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_TYPE, default='ovulation_induction_intercourse',
                            string='Type')
    consultant = fields.Char(string='Consultant')
    oral_drugs = fields.Char(string='Oral Drugs')
    down_regulation = fields.Char(string='Down Regulation')
    superovulation = fields.Char(string='Superovulation')
    ovarian_response = fields.Char(string='Ovarian Response')
    outcome = fields.Char(string='Outcome')
