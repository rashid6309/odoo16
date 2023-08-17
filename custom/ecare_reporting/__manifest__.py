{
    'name': 'eCare Reporting',
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
    'depends': ['base', 'mail', 'ecare_core','ecare_appointment', 'report_xlsx', 'ecare_invoicing'],
    'demo': [],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Static files
        'data/paper_format.xml',

        # Reports here
        'reports/services_report.xml',
        'reports/ec_slot_reporting.xml',
        'reports/ec_cash_report.xml',
        'reports/ec_cash_due_report.xml',
        'reports/ec_services_report.xml',
        'reports/ec_patient_profile_report.xml',

        # Views

        'views/reports.xml',
        'views/account_move.xml',
        'views/reporting_view.xml',
        'views/patient.xml',

        # Menu
        'data/menus.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ecare_reporting/static/src/js/reporting.js',
            'ecare_reporting/static/src/js/amount_due.js',
            'ecare_reporting/static/src/js/services.js',
            'ecare_reporting/static/src/xml/reporting.xml',
            'ecare_reporting/static/src/xml/amount_due_reporting.xml',
            'ecare_reporting/static/src/xml/services.xml',
            'ecare_reporting/static/src/css/reporting.css',
        ],

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
