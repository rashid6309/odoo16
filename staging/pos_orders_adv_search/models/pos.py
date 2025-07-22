# -*- coding: utf-8 -*-

from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError, ValidationError

import logging

_logger = logging.getLogger(__name__)


class PosConfig(models.Model):
    _inherit = "pos.config"

    allow_invoice_number_search = fields.Boolean(default=True)
    allow_order_ref_search = fields.Boolean(default=True)


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_allow_invoice_number_search = fields.Boolean(
        related="pos_config_id.allow_invoice_number_search", readonly=False
    )
    pos_allow_order_ref_search = fields.Boolean(related="pos_config_id.allow_order_ref_search", readonly=False)


class PosSession(models.Model):
    _inherit = "pos.session"

    def _pos_data_process(self, loaded_data):
        super()._pos_data_process(loaded_data)
        loaded_data["account_move_by_id"] = {
            account_move["id"]: account_move for account_move in loaded_data["account.move"]
        }

    def _pos_ui_models_to_load(self):
        result = super()._pos_ui_models_to_load()
        new_model = "account.move"
        if new_model not in result:
            result.append(new_model)
        return result

    def _loader_params_account_move(self):
        return {
            "search_params": {
                "domain": [("pos_order_ids", "!=", False)],
                "fields": ["name", "ref"],
            },
        }

    def _get_pos_ui_account_move(self, params):
        return self.env["account.move"].search_read(**params["search_params"])


class POSOrder(models.Model):
    _inherit = "pos.order"

    def get_invoice(self):
        self.ensure_one()
        return {"id": self.account_move.id, "name": self.account_move.name, "ref": self.account_move.ref}
