{
    'name': 'eCare Medical History',
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
    'depends': ['base', 'mail', 'ecare_core'],
    'demo': [],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Menu
        'data/menus.xml',

        # Reports here


        # Views
        'views/female_obstetrics_history.xml',

        'views/ec_patient.xml',
        'views/ec_procedure.xml',

        # This Views should be below after all of its views.
        'views/first_consultation.xml',

    ],
    'assets': {
        'web.assets_backend': [
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
