# -*- coding: utf-8 -*-
{
    "name": "POS Orders Custom Search",
    "version": "16.0.0.0.0",
    "summary": """POS Orders search by invoice number & Order Ref""",
    "description": """POS Orders search by invoice number & Order Ref""",
    "category": "Point of Sale",
    "license": "OPL-1",
    "price": 20.0,
    "currency": "EUR",
    "author": "HMPRO",
    "website": "",
    "depends": ["point_of_sale"],
    "data": [
        "views/pos_view.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_orders_adv_search/static/src/js/**/*",
            "pos_orders_adv_search/static/src/xml/**/*",
        ]
    },
    "images": ["static/description/banner.png"],
    "installable": True,
    "application": True,
    "auto_install": False,
}
