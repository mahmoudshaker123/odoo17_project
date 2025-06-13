{
    'name': "IET Task Two",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','hr',
                ],
    'data': [
        'security/security.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv',
        'views/employee_number_view.xml',
        'views/task_management_view.xml',

        ],
    'installable': True,
    'application': True,

}
