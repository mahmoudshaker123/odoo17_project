{
    'name': "Itplus Sale Order",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base', 'sale', 'sale_management', 'mrp'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_item_view.xml',
        'views/related_sale_order_line_inhert.xml',
        'wizard/add_sale_item_wizard_view.xml',
              ],
    'installable': True,
    'application': True,

}
