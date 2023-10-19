from odoo import models, fields


class LabHistory(models.Model):
    _name = "ec.lab.history"
    _description = "Patient Lab History"


    female_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")
    male_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete="restrict")

    name = fields.Char(string="Name", required=True)
    date = fields.Date(string="Date")

    filename = fields.Char(string="Filename")
    attachment_id = fields.Binary(string="Attachments",
                                  help="If you want to upload any attachment.")

    # attachment_ids = fields.Many2many(comodel_name="ir.attachment",
    #                                   column1="lab_id",
    #                                   column2="attachment_id",
    #                                   relation="lab_history_attachment_id",
    #                                   string="Attachments",
    #                                   help="If you want to upload any attachment.")
