{
    'name': "Maintenance Contracts",
    'author': "IT Plus Egypt",
    'category': 'Administration',
    'version': '17.0.1.0.1',
    'depends': ['base', 'sale', 'hr', 'mail', 'maintenance', 'web',
                ],
    'data': [
        "security/ir.model.access.csv",
        "views/maintenance_view.xml",
        "views/base_menu.xml",
        "views/history_view.xml",
    ],
    'images': ['static/description/icon.png'],
    'assets': {
        'web.assets_backend': [
            'maintenance_contracts/static/src/css/styles.css',
        ],
    },
    'license': 'LGPL-3',

    'installable': True,
    'application': True,
}
