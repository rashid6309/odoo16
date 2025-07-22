{
    'name': 'Screen Lock using PIN',
    'version': '16.0.1.0.0',
    'category': 'Tools',
    'summary': 'Add screen lock functionality using PIN for Odoo 16',
    'author': 'Your Name',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/screen_lock_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'screen_lock/static/src/js/screen_lock.js',
            'screen_lock/static/src/css/screen_lock.css',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}