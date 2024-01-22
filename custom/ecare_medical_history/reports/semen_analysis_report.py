from odoo import models

class SemenAnalysisHospitalRecord(models.AbstractModel):
    _name = 'report.ecare_medical_history.ec_semen_analysis_doc'
    _description = 'Semen Analysis Report: Hospital Record'

    def _get_report_values(self, docids, data=None):
        docs = self.env['ec.semen.analysis'].browse(docids)

        return {
            'doc_ids': docs.ids,
            'doc_model': 'ec.semen.analysis',
            'company': self.env.user.company_id,
            'docs': docs,
        }



