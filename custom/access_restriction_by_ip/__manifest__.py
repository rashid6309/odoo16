# -*- coding: utf-8 -*-

{
    'name': 'Access Restriction By IP',
    'summary': """User Can Access His Account Only From Specified IP Address""",
    'version': '16.0.1.0.0',
    'description': """User Can Access His Account Only From Specified IP Address""",
    'author': 'Rashid Noor',
    'company': 'Tangent Technologies',
    'website': 'http://tangenttek.com/',
    'category': 'Tools',
    'depends': ['base', 'mail', 'ecare_appointment'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'security/ec_security.xml',
        'views/allowed_ips_view.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
}

