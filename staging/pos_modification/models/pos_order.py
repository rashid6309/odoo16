from itertools import groupby
from collections import defaultdict
from odoo import api, fields, models, _
from odoo.tools import float_is_zero, float_compare
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.model
    def _create_picking_from_pos_order_lines(
        self, location_dest_id, lines, picking_type, partner=False
    ):

        locations = lines.mapped("location_id")
        pickings = self.env["stock.picking"]
        if not locations:
            return super(StockPicking, self)._create_picking_from_pos_order_lines(
                location_dest_id, lines, picking_type, partner
            )

        for location in locations:

            stockable_lines = lines.filtered(
                lambda l: l.location_id.id == location.id
                and l.product_id.type in ["product", "consu"]
                and not float_is_zero(
                    l.qty, precision_rounding=l.product_id.uom_id.rounding
                )
            )
            if not stockable_lines:
                return pickings
            positive_lines = stockable_lines.filtered(lambda l: l.qty > 0)
            negative_lines = stockable_lines - positive_lines

            if positive_lines:
                location_id = picking_type.default_location_src_id.id
                positive_picking = self.env["stock.picking"].create(
                    self._prepare_picking_vals(
                        partner, picking_type, location.id, location_dest_id
                    )
                )

                positive_picking._create_move_from_pos_order_lines(positive_lines)
                try:
                    with self.env.cr.savepoint():
                        positive_picking._action_done()
                except (UserError, ValidationError):
                    pass

                pickings |= positive_picking
            if negative_lines:
                if picking_type.return_picking_type_id:
                    return_picking_type = picking_type.return_picking_type_id
                    return_location_id = location.id
                else:
                    return_picking_type = picking_type
                    return_location_id = location.id

                negative_picking = self.env["stock.picking"].create(
                    self._prepare_picking_vals(
                        partner,
                        return_picking_type,
                        location_dest_id,
                        return_location_id,
                    )
                )
                negative_picking._create_move_from_pos_order_lines(negative_lines)
                try:
                    with self.env.cr.savepoint():
                        negative_picking._action_done()
                except (UserError, ValidationError):
                    pass
                pickings |= negative_picking
        return pickings


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            order_id = self.env["pos.order"].browse(vals.get("order_id"))
            default_location_id = (
                order_id.config_id.picking_type_id.default_location_src_id.id
            )
            if not vals.get("location_id"):
                vals.update(location_id=default_location_id)
        return super(PosOrderLine, self).create(vals_list)

    location_id = fields.Many2one(comodel_name="stock.location", string="Location")
    warehouse_id = fields.Many2one(
        comodel_name="stock.warehouse",
        related="location_id.warehouse_id",
        string="Warehouse",
    )

    def _prepare_refund_data(self, refund_order, PosOrderLineLot):
        res = super(self, PosOrderLine)._prepare_refund_data(
            refund_order, PosOrderLineLot
        )
        res.update(
            location_id,
            self.location_id.id
            if self.location_id
            else refund_order.config_id.picking_type_id.default_location_src_id.id,
        )
        return res
