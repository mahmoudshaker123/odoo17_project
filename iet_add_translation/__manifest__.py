

{
    'name': "IET Add Translation",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','sale_management','sale',
                ],
    'data': [
        'views/add_translation_inherit_view.xml',
        'reports/tax_invoice_ksa.xml',

        ],
'assets': {
        'web.report_assets_common':['iet_add_translation/static/src/css/font.css']
    },

    'application': True,
}
