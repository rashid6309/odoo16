{
    'name': 'eCare',
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
    'depends': ['base', 'mail'],
    'demo': [],
    'data': [
        'security/ir.model.access.csv',

        'data/data.xml',
        'data/system_parameter.xml',
        # Views
        'views/third_party_api_log.xml',
        'views/ec_patient.xml',

        'reports/ec_patient_reporting.xml',

        # Data
        'data/menu.xml'

    ],
    'assets': {
        'web.assets_backend': [
            'ecare_core/static/src/xml/chatter_topbar_custom.xml',
            # 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.css',
            # 'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.pkgd.js'
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
