{
    'name': 'eCare Invoicing',
    'version': '1.0.0',
    'category': 'Healthcare',
    'summary': 'Healthcare',
    'description': 'Healthcare',
    'live_test_url': '',
    'sequence': '1000',
    'website': '',
    'author': 'Tangent Technologies',
    'maintainer': 'Rashid Noor',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['base', 'mail', 'ecare_core', 'account', 'ecare_appointment'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'reports/core_reports.xml',
        'reports/ec_invoicing_reporting.xml',
        'reports/payment_report.xml',

        'views/account_payment_register.xml',
        'views/account_payment.xml',
        'views/ec_invoicing.xml',
        'views/product_template.xml',
        'views/account_move_line_history_view.xml',
        'views/credit_note_views.xml',
        'views/account_move_reversal.xml',

        'views/ec_patient.xml',

        'data/core_action.xml',
        'data/menus.xml',

    ],
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            'ecare_invoicing/static/src/xml/templates_inherited.xml',
            'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.css',
            'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.pkgd.js'
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
