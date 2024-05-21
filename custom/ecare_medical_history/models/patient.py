from odoo import models, fields, api, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.tools.misc import get_lang


class EcMedicalPatient(models.Model):
    _inherit = "ec.medical.patient"

    # patient_treatment_pathways_current = fields.Selection(selection=StaticMember.REPEAT_TREATMENT_ADVISED_LIST,
    #                                                       string='Treatment Pathway')

    def _compute_next_visit(self):
        date = fields.Datetime.now()
        for rec in self:
            appointment_id = self.env['ec.booked.slot.record'].search(
                domain=[('partner_id', '=', rec.id),
                        ('state', '=', 'Booked'),
                        ('date', '>=', date.today())],
                order="date asc",
                limit=1
            )
            visit = "Not Scheduled"
            if appointment_id:
                date_format = (self.env['res.lang']._lang_get(self.env.user.lang).date_format
                               or get_lang(self.env).date_format)

                visit = f'{appointment_id.date.strftime(date_format)} {appointment_id.start}'

            return visit

    @api.model
    def get_selection_label(self, field_name, field_value):
        """ Returns the display name of a selection field value. """
        field = self.env['ec.patient.timeline']._fields[field_name]
        if field and field_value:
            return dict(field.selection).get(field_value)
        return None

    @api.model
    def get_banner_data_values(self, patient_id):
        patient = self.search(domain=[('id', '=', patient_id)])
        patient_timeline = self.env['ec.patient.timeline'].search(domain=[
            ('timeline_patient_id', '=', int(patient.id))
        ], limit=1)
        values = {
            'next_visit': patient._compute_next_visit(),
            'current_treatment_pathways': self.get_selection_label('patient_treatment_pathways_current', patient_timeline.patient_treatment_pathways_current) or None
        }
        return values