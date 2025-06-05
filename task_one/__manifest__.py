{
    'name': "IET Task One",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','sale_management','sale','stock',
                ],
    'data': [
        'views/account_move_view.xml',
        'reports/delivery_order_inherit_report.xml',
        'reports/custom_invoice_report.xml',

        ],
    'installable': True,
    'application': True,

}
