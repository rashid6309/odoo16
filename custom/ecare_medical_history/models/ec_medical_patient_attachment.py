from odoo import models, fields, api


class MedicalPatientAttachment(models.Model):
    _name = "ec.medical.patient.attachment"
    _description = "Patient Attachments"
    _order = 'create_date desc'

    patient_attachment_timeline_id = fields.Many2one(comodel_name="ec.patient.timeline", ondelete="restrict")

    name = fields.Char(string="Details", required=True)

    attachment_id = fields.Many2many('ir.attachment',
                                     'patient_attachment_document_rel',
                                     'patient_attachment_id',
                                     'doc_id',
                                     help="If you want to upload any attachment.",
                                     string='Document', public=True, copy=False)

    results = fields.Text('Results')

    @api.model
    def create(self, vals):
        templates = super(MedicalPatientAttachment, self).create(vals)
        # fix attachment ownership
        for template in templates:
            if template.attachment_id:
                template.attachment_id.write({'res_model': self._name, 'res_id': template.id})
        return templates

