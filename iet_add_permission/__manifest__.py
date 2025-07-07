

{
    'name': "IET Add Permissions",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','sale_management','sale',
                ],
    'data': [
        'security/product_groups.xml',
        'security/sales_team_groups.xml',
        'security/sales_team_rules.xml',
        'security/customer_groups.xml',
        'security/ir.model.access.csv',

    ],

    'application': True,
}
