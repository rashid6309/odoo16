# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details
{
    'name': 'Moyasar Payment Gateway',
    'version': '16.0.0.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 1,
    'summary': 'Odoo Moyasar Payment Gateway',
    'description': 'Odoo Moyasar Payment Gateway',
    'author': 'Bizople Solutions Pvt. Ltd.',
    'website': 'https://www.bizople.com/',
    'depends': ['base','website_sale'],
    'data': [
        'views/moyasar_form.xml',
        'data/moyasar_data.xml',
        'views/payment_acquirer.xml',
        'views/payment_transaction_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'payment_moyasar_bizople/static/src/scss/moyasar_form.scss',
            'payment_moyasar_bizople/static/src/js/moyasar_form.js',
            'payment_moyasar_bizople/static/src/js/payment_mixin.js',
        ],
    },
    'images': [
        'static/description/banner.png'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'OPL-1',
    'price' : 100,
    'currency': 'EUR',
    'external_dependencies': {
        "python" : ["moyasar"],
    },
}
