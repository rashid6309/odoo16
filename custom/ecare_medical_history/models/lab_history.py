from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.validation import Validation


class LabHistory(models.Model):
    _name = "ec.lab.history"
    _description = "Patient Lab History"
    _order = 'date desc'

    female_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")
    male_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")

    filename = fields.Char(string="Filename")
    attachment_id = fields.Many2many('ir.attachment', 'lab_history_document_rel',
                                     'lab_id', 'doc_id', help="If you want to upload any attachment.",
                                     string='Document')

    results = fields.Text('Results', required=True)

    # attachment_ids = fields.Many2many(comodel_name="ir.attachment",
    #                                   column1="lab_id",
    #                                   column2="attachment_id",
    #                                   relation="lab_history_attachment_id",
    #                                   string="Attachments",
    #                                   help="If you want to upload any attachment.")

    @api.onchange('date')
    def _check_lab_date(self):
        if self.date:
            return Validation._date_validation(self.date)

    @api.model
    def create(self, vals):
        templates = super(LabHistory, self).create(vals)
        # fix attachment ownership
        for template in templates:
            if template.attachment_id:
                template.attachment_id.write({'res_model': self._name, 'res_id': template.id})
        return templates

