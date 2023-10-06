{
    'name': 'eCare User Management',
    'version': '1.0.0',
    'category': 'Healthcare - User Management',
    'summary': 'Healthcare',
    'description': 'Healthcare',
    'live_test_url': '',
    'sequence': '1000',
    'website': '',
    'author': 'Tangent Technologies',
    'maintainer': 'Umar Azam',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['ecare_appointment', 'ecare_invoicing', 'ecare_reporting', 'document_management'],
    'demo': [],
    'data': [
        'security/user_management.xml',
        'security/document_management.xml',
        'security/invoicing.xml',
        'security/ir.model.access.csv',

        # Menu's
        'menu/menu.xml',
        'menu/appointment.xml',
        'menu/configuration.xml',
        'menu/invoicing.xml',
        'menu/report.xml',

        # Views
        'views/account_move.xml',

    ],
    'assets': {
        'web.assets_backend': [
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
