from odoo import models, fields, api, _


class EcMedicalPatient(models.Model):
    _inherit = "ec.medical.patient"

    def _compute_next_visit(self):
        date = fields.Datetime.now()
        for rec in self:
            appointment_id = self.env['ec.booked.slot.record'].search(
                domain=[('partner_id', '=', rec.id),
                        ('date', '>=', date.today())],
                order="date asc",
                limit=1
            )
            visit = "Not Scheduled"
            if appointment_id:
                visit = f'{appointment_id.date} {appointment_id.start}'

            return visit

    @api.model
    def get_banner_data_values(self, patient_id):
        patient = self.search(domain=[('id', '=', patient_id)])
        values = {
            'next_visit': patient._compute_next_visit()
        }
        return values