import re
import json

from odoo import models, fields, api


class PosSession(models.Model):
    _inherit = "pos.session"

    custom_analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Custom Analytic Account",
        related="config_id.custom_analytic_account_id",
    )

    def _get_pos_ui_stock_location(self, params):
        return self.env["stock.location"].search_read(**params["search_params"])

    def _loader_params_stock_location(self):
        return {
            "search_params": {
                "domain": [
                    ("usage", "=", "internal"),
                    ("warehouse_id", "=", self.config_id.warehouse_id.id),
                ],
                "fields": ["id", "name", "company_id"],
            }
        }

    @api.model
    def _pos_ui_models_to_load(self):
        models_to_load = super(PosSession, self)._pos_ui_models_to_load()
        models_to_load.append("stock.location")
        return models_to_load

    def _loader_params_product_product(self):
        res = super(PosSession, self)._loader_params_product_product()
        fields = res["search_params"]["fields"]
        fields.extend(["stock_quant_ids", "free_qty", "qty_available"])
        res["search_params"]["fields"] = fields
        return res
