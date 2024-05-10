from odoo import models, fields, api, _
from odoo.tools.misc import get_lang


class EcMedicalPatient(models.Model):
    _inherit = "ec.medical.patient"

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
    def get_banner_data_values(self, patient_id):
        patient = self.search(domain=[('id', '=', patient_id)])
        values = {
            'next_visit': patient._compute_next_visit(),
            'current_treatment_pathways': patient._compute_next_visit()
        }
        return values