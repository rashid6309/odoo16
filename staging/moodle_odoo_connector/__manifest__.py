{
    'name': 'Moodle Odoo Connector',
    'version': '1.0.0',
    'category': 'Education Connector',
    'summary': 'Education',
    'description': 'Education',
    'live_test_url': '',
    'sequence': '1000',
    'website': '',
    'author': 'Tangent Technologies',
    'maintainer': 'Rashid Noor',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['base', 'mail',],
    'demo': [],
    'data': [
        # Security
        # 'security/ir_groups.xml',
        'security/security.xml',
        'security/ir.model.access.csv',

        # Menu
        # 'data/menus.xml',

        # Reports here

        # Views - Independent

        # 'data/ec_medical_multi_selection_data.xml',

        # Views
        'views/moodle_config_view.xml',
        'views/moodle_course.xml',
        'views/moodle_student.xml',


    ],
    'assets': {
        'web.assets_backend': [
            # '/moodle_odoo_connector/static/src/js/custom.js',
            # 'moodle_odoo_connector/static/src/css/custom.css',  # FIX: Issue in the header in the overall system

        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
