

{
    'name': "App One",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/property_view.xml',
        'views/owner_view.xml',
        'views/tag_view.xml'


],
    'assets': {
        'web.assets_backend':['app_one/static/src/css/property.css']
    },

    'application': True,
}
