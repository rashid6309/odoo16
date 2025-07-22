from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    # pos_location_id = fields.Many2one(related="pos_config_id.location_id", readonly=False)
    pos_discount_fx = fields.Float(related="pos_config_id.discount_fx", readonly=False)
    pos_custom_analytic_account_id = fields.Many2one(
        "account.analytic.account",
        related="pos_config_id.custom_analytic_account_id",
        readonly=False,
    )


class PosConfig(models.Model):
    _inherit = "pos.config"

    location_id = fields.Many2one(
        comodel_name="stock.location", compute="_compute_default_location_id"
    )
    discount_fx = fields.Float(string="Fixed Discount", default=10.0)

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account", string="Custom Analytic Account"
    )

    @api.depends("picking_type_id")
    def _compute_default_location_id(self):
        for rec in self:
            rec.location_id = rec.picking_type_id.default_location_src_id.id
