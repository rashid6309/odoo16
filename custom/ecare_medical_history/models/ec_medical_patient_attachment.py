from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.validation import Validation


class MedicalPatientAttachment(models.Model):
    _name = "ec.medical.patient.attachment"
    _description = "Patient Attachments"
    _order = 'create_date desc'

    patient_attachment_timeline_id = fields.Many2one(comodel_name="ec.patient.timeline", ondelete="restrict")

    name = fields.Char(string="Name", required=True)

    attachment_id = fields.Many2many('ir.attachment', 'patient_attachment_document_rel',
                                     'patient_attachment_id', 'doc_id', help="If you want to upload any attachment.",
                                     string='Document')

    results = fields.Text('Results')

