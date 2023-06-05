from odoo import models, fields


class ThirdPartyApiLogs(models.Model):
    _name = "third.party.api.log"
    _description = "Third Party "
    _order = "create_date desc"

    name = fields.Char(string="Name")
    url = fields.Char(string="URL")
    payload = fields.Char(string="Payload")
    response = fields.Char(string="Response")
