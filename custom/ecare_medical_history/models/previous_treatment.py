from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalPreviousHistory(models.Model):
    _name = 'ec.medical.previous.treatment'
    _description = "Previous Treatment"
    _order = "create_date desc, id asc"

    timeline_id = fields.Many2one('ec.patient.timeline', string='Patient Timeline')
    patient_id = fields.Many2one(comodel_name="ec.medical.patient", string="Patient")

    type = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_TYPE,
                            string='Type')
    consultant_id = fields.Many2one(comodel_name="res.consultant",
                                 ondelete='restrict',
                                 required=False,
                                 string='Consultant')
    oral_drugs = fields.Text(string='Oral Drugs')
    treatment_notes = fields.Text(string='Notes')
    down_regulation = fields.Text(string='Down Regulation')
    superovulation = fields.Text(string='Superovulation')
    ovarian_response = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_RESPONSE,
                                        string='Ovarian Response')
    outcome = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_OUTCOME,
                               string='Outcome')

    treatment_of = fields.Selection(selection=StaticMember.PREVIOUS_TREATMENT_OF,
                                    string='Treatment of')

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
