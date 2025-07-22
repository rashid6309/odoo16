{
    "name": "POS Modifications",
    "summary": """POS Modifications""",
    "description": """POS Modifications""",
    "author": "My Company",
    "website": "https://www.yourcompany.com",
    "category": "Point of Sales",
    "version": "16.0.1.0.7",
    "depends": ["point_of_sale", "stock", "pos_discount", "pos_analytic_account_app"],
    "data": [
        "views/res_config_settings.xml",
    ],
    "assets": {
        "point_of_sale.assets": [
            "pos_modification/static/src/js/models.js",
            "pos_modification/static/src/js/FixedDiscountButton.js",
            "pos_modification/static/src/xml/**/*",
        ],
    },
    "license": "LGPL-3",
}
