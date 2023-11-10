{
    'name': 'eCare Medical History',
    'version': '1.0.0',
    'category': 'Healthcare - Medical History',
    'summary': 'Healthcare',
    'description': 'Healthcare',
    'live_test_url': '',
    'sequence': '1000',
    'website': '',
    'author': 'Tangent Technologies',
    'maintainer': 'Rashid Noor',
    'license': 'LGPL-3',
    'support': '',
    'depends': ['web', 'base', 'mail', 'ecare_core', 'ecare_appointment'],
    'demo': [],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Menu
        'data/family_history_data.xml',
        'data/menus.xml',

        # Reports here

        # Views - Independent
        'views/health_center.xml',
        'views/investigation.xml',
        'views/factors.xml',
        'views/treatment_list.xml',
        'data/ec_medical_multi_selection_data.xml',
        
        # Views
        'views/female_obstetrics_history.xml',
        'views/previous_treatment.xml',

        # 'views/ec_patient.xml', # not being used now.
        'views/ec_procedure.xml',
        'views/lab_history.xml',

        # This Views should be below after all of its views.

        # Repeat
        'views/repeat_consultation.xml',

        # TVS
        'views/ec_medical_tvs.xml',
        # Timeline
        'views/patient_timeline.xml',

        # Timeline Wizard
        'views/ec_patient_timeline_wizard.xml',

        # Semen Anlysis
        'views/semen_analysis.xml',

        # Reports
        'reports/semen_analysis_report.xml',
        'reports/patient_report.xml',

        # This should be called at the end
        'data/view_menus.xml',


    ],
    'assets': {
        'web.assets_backend': [
            '/ecare_medical_history/static/src/js/generic.js',
            '/ecare_medical_history/static/src/js/custom.js',
            'ecare_medical_history/static/src/css/custom.css', # FIX: Issue in the header in the overall system
            'ecare_medical_history/static/src/css/scan_view.css',
            'ecare_medical_history/static/src/xml/summary.xml',
            'ecare_medical_history/static/src/xml/banner_template.xml'
        ],


    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
