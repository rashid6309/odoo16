{
    'name': 'eCare Appointment',
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
    'depends': ['base', 'mail', 'contacts', 'ecare_core', 'account'],
    'demo': [],
    'data': [
        'security/ec_security.xml',
        'security/ir.model.access.csv',

        'data/menus.xml',
        'data/ecare_menu.xml',

        'views/health_center.xml',
        'views/investigation.xml',
        'views/treatment_list.xml',
        'views/consultant.xml',
        'views/consultation_type.xml',

        'views/primary_category.xml',
        'views/category.xml',
        'views/sub_category.xml',
        'views/common_views_categories.xml',

        'views/configurator.xml',
        'views/schedule.xml',

        'views/block_slot.xml',

        'views/slots_record.xml',
        'views/slot_record_block.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ecare_appointment/static/src/css/dashboard.css',
            'ecare_appointment/static/src/js/icsi.js',
            'ecare_appointment/static/src/css/lib/nv.d3.css',
            'ecare_appointment/static/src/js/lib/d3.min.js',
            # 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.8.0/Chart.bundle.js',
            'ecare_appointment/static/src/xml/dashboard.xml',
            # 'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.css',
            # 'https://cdnjs.cloudflare.com/ajax/libs/flickity/1.0.0/flickity.pkgd.js'
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
