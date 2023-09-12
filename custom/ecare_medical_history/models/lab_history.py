from odoo import models, fields


class LabHistory(models.Model):
    _name = "ec.lab.history"
    _description = "Patient Lab History"


    female_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation")
    male_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation")

    name = fields.Char(string="Name")
    date = fields.Date(string="Date")
    attachment_ids = fields.Many2many(comodel_name="ir.attachment",
                                      column1="lab_id",
                                      column2="attachment_id",
                                      relation="lab_history_attachment_id",
                                      string="Attachments",
                                      help="If you want to upload any attachment.")
