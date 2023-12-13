from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalPreviousHistory(models.Model):
    _name = 'ec.medical.previous.treatment'
    _description = "Previous Treatment"
    _order = "create_date desc"

    timeline_id = fields.Many2one('ec.patient.timeline', string='Patient Timeline')
    patient_id = fields.Many2one(comodel_name="ec.medical.patient", string="Patient")

    type = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_TYPE,
                            string='Type')
    consultant = fields.Char(string='Consultant')
    oral_drugs = fields.Char(string='Oral Drugs')
    down_regulation = fields.Char(string='Down Regulation')
    superovulation = fields.Char(string='Superovulation')
    ovarian_response = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_RESPONSE,
                                        string='Ovarian Response')
    outcome = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_OUTCOME,
                               string='Outcome', required=True)

    treatment_of = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_OF,
                                    string='Treatment of', required=True)

    def action_open_form_view(self, patient_id, timeline_id=None):
        context = {
            'default_patient_id': patient_id.id,
            'default_timeline_id': timeline_id.id if timeline_id else None
        }
        domain = [
            '|',
            ('patient_id', '=', patient_id.id),
            ('timeline_id', '=', timeline_id.id if timeline_id else None)
        ]
        return {
            "name": _("Previous Treatment"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.medical.previous.treatment',
            'view_id': self.env.ref('ecare_medical_history.previous_treatment_tree_read_only_view').id,
            'view_mode': 'tree',
            "target": 'new',
            'context': context,
            'domain': domain,
        }
