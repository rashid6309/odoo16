

{
    'name': 'Point of Sale Receipt',
    'category': 'Sales/Point of Sale',
    'summary': 'Add a button to print the receipt with information such as: '
               'product name, internal reference, qty, location',
    'description': "",
    'depends': ['point_of_sale', 'pos_modification'],
    'license': 'LGPL-3',
    'installable': True,
    'auto_install': True,
    'author': 'Linh Nguyen',
    'assets': {
        'point_of_sale.assets': [
            'pos_receipt/static/src/js/models.js',
            'pos_receipt/static/src/js/PosReceiptButton.js',
            'pos_receipt/static/src/xml/PosReceiptButton.xml',
            'pos_receipt/static/src/xml/ProductInfoPopup.xml'
        ],
    }
}