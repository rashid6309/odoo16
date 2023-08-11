from odoo import models


class EcarePatient(models.Model):
    _inherit = "ec.medical.patient"

    def action_patient_profile_print_report(self):
        return self.env.ref('ecare_reporting.ec_patient_profile_report').report_action(self)
