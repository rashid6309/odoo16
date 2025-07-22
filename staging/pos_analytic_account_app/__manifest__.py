{
    "name": "POS Analytic Account",
    "author": "Edge Technologies",
    "version": "16.0.1.0",
    "live_test_url": "https://youtu.be/mRVMX9qUUkI",
    "images": ["static/description/main_screenshot.png"],
    "summary": "Assign analytic account on pos session analytic account on pos order analytic account on point of sales analytic account on point of sale analytic account on pos invoice analytic costing on pos accounting entry analytic account on pos session.",
    "description": """This module helps to assign analytic account and it's tags to 
                       pos session ,pos order and related payments ,journal entries ,journal items and it's invoices.""",
    "license": "OPL-1",
    "depends": ["base", "point_of_sale", "account"],
    "data": [
        "security/ir.model.access.csv",
        "views/custom_pos_analytic_account.xml",
    ],
    "auto_install": False,
    "installable": True,
    "price": 10,
    "currency": "EUR",
    "category": "Point of Sales",
}
