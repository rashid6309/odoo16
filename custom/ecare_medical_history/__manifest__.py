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

        # Reports here

        # Views

        'views/first_consultation.xml',
        'views/female_obstetrics_history.xml',

        # Menu
        'data/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.css',
            'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.pkgd.js',
            'ecare_reporting/static/src/css/reporting.css',
            'ecare_medical_history/static/src/js/*',
            'ecare_medical_history/static/src/css/*',
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
