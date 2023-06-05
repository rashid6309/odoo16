from odoo import models, fields, api


class AccountMOveLine(models.Model):
    _inherit = "account.move.line"

    inverse_balance = fields.Monetary(string="Balance",
                                      store="True",
                                      compute="_compute_inverse_balance")

    @api.depends("balance")
    def _compute_inverse_balance(self):
        for line in self:
            line.inverse_balance = -1 * line.balance
