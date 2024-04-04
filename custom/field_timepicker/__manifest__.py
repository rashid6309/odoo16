
{
    'name': 'Field Time Picker',
    'version': '16.0.1.0.0',
    'summary': 'Time Picker Widget Using Wickedpicker',
    'description': 'Field Time Picker enhances the time input functionality in '
                   'Odoo',
    'category': 'Extra Tools',
    'author': 'Rashid Noor',
    'company': 'Tangent Technologies',
    'maintainer': 'Tangent Technologies',
    'depends': ['base'],
    'website': 'https://www.tangenttek.com/',
    'data': [],
    "assets": {
        'web.assets_backend': [
            'field_timepicker/static/wickedpicker/stylesheets/wickedpicker.css',
            'field_timepicker/static/wickedpicker/src/wickedpicker.js',
            'field_timepicker/static/src/xml/timepicker.xml',
            'field_timepicker/static/src/js/time_widget.js',
        ],
    },
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
