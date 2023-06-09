from odoo import models, fields


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # CRITICAL: Do know if you change the sequence here it'll have impact on the invoice line sequence.
    TYPE_SELECTION = [("Hospital Services", "Hospital Services"),
                      ("Pharmacy", "Pharmacy"),
                      ('Laboratory', "Laboratory"),
                      ("Radiology", "Radiology")]

    service_type = fields.Selection(selection=TYPE_SELECTION,
                                    string="Type",
                                    tracking=True)

    unit_price_editable = fields.Boolean(string="Allow Price Editable",
                                          required=True,
                                          default=0)
