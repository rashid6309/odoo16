from odoo import models, fields, _, api
# 11:20AM -- 11-05-2023


class DocumentAttachment(models.Model):
    _name = "document.management"
    _description = "Document Management"

    _order = "write_date desc, id desc"

    name = fields.Char(string="Document Name",
                       copy=False,
                       required=True)

    attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                      relation="doc_attach_rel",
                                      column1="doc_id",
                                      column2="attach_id",
                                      string="Attachment",
                                      copy=False)

    issue_date = fields.Datetime(string='Issue Date', default=fields.datetime.now(), copy=False)
    expiry_date = fields.Date(string='Expiry Date', copy=False)

    active = fields.Boolean(default=True)

    # FK where this will be used we can inherit as well.
    patient_id = fields.Many2one(comodel_name="ec.medical.patient", copy=False, ondelete='restrict')

    @api.model_create_multi
    def create(self, vals_list):
        record = super(DocumentAttachment, self).create(vals_list)
        if record.patient_id:
            record.patient_id.update_write_date()
        return  record

    def write(self, vals_list):
        record = super(DocumentAttachment, self).write(vals_list)
        if self.patient_id:
            self.patient_id.update_write_date()
        return  record


class Patient(models.Model):
    _inherit = "ec.medical.patient"

    document_count = fields.Integer(compute='_document_count', string='# Documents')

    def _document_count(self):
        for each in self:
            document_ids = self.env['document.management'].sudo().search([('patient_id', '=', each.id)])
            each.document_count = len(document_ids)

    def document_view(self):
        self.ensure_one()

        action = self.env["ir.actions.actions"]._for_xml_id("document_management.document_management_action")

        context = self._context.copy()
        context.update(
            {'default_patient_id': self.id}
        )
        action['context'] = context

        return {
            "name": _("Documents "),
            "type": 'ir.actions.act_window',
            "res_model": 'document.management',
            'view_mode': 'tree,form',
            "target": 'current',
            "domain": [('patient_id', '=', self.id)],
            "context": context
        }

        return action
