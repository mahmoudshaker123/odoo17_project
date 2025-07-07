

{
    'name': "IET Job Order",
    'author': "Mahmoud Shaker",
    'category': '',
    'version': '17.0.0.1.0',
    'depends': ['base','mrp',
                ],
    'data': [
        'security/ir.model.access.csv',
        'views/job_order_view.xml',
        'data/sequence.xml',


        ],

    'application': True,
}
