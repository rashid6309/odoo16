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
        'security/ir_groups.xml',
        'security/ir.model.access.csv',

        # Menu
        'data/family_history_data.xml',
        'data/menus.xml',
        'data/semen_analysis_sequence.xml',
        'data/years_data.xml',

        # Reports here

        # Views - Independent
        'views/health_center.xml',
        'views/medical_labs.xml',
        'views/investigation.xml',
        'views/ec_medical_profession.xml',
        'views/ec_medical_education.xml',
        'views/year.xml',
        'views/factors.xml',
        'views/treatment_list.xml',
        'views/ec_medical_dianosis.xml',
        'views/ec_medical_investigation.xml',
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


        # Treatment Pathway Wizard
        'views/treatment_pathway_wizard.xml',
        'views/ec_medical_oi_ti_platform_cycle.xml',
        'views/ec_medical_oi_ti_platform_attempt.xml',

        # Semen Anlysis
        'views/semen_analysis.xml',
        
        # Pregnancy
        'views/ec_medical_pregnancy.xml',

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
            'ecare_medical_history/static/src/xml/banner_template.xml',
        ],
        

    },
    'installable': True,
    'application': True,
    'auto_install': False,
    # 'images': ['static/description/banner.png'],
}
