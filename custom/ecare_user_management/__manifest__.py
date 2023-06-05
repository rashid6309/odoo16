{
    'name': 'eCare User Management',
    'version': '1.0.0',
    'category': 'Healthcare',
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
        'security/document_managment.xml',
        'security/ir.model.access.csv',

        # Menu's
        'menu/menu.xml',
        'menu/appointment.xml',
        'menu/configuration.xml',
        'menu/customer.xml',
        'menu/report.xml',
    ],
    'assets': {
        'web.assets_backend': [
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
