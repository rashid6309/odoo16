import json
from odoo import api, fields, models, _


class Product(models.Model):
    _inherit = "product.product"

    def get_product_info_pos(self, price, quantity, pos_config_id):
        res = super(Product, self).get_product_info_pos(price, quantity, pos_config_id)
        config = self.env["pos.config"].browse(pos_config_id)
        domain = [
            ("product_id", "=", self.id),
            ("location_id.warehouse_id", "=", config.picking_type_id.warehouse_id.id),
        ]
        stock_quant_ids = self.env["stock.quant"].search(domain)
        res.update(
            quants=[
                {
                    "id": s.location_id.id,
                    "name": s.location_id.display_name,
                    "quantity": s.quantity,
                }
                for s in stock_quant_ids
            ]
        )
        return res
