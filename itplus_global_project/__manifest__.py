# -*- coding: utf-8 -*-
{
    'name': 'Global Project',
    'version': '17.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Global Project Management',
    'description': """
        Global Project Management System
        Features:
        - Daily BOM Management
        - Quality Management System
        - Stock Quality Control
        - Manufacturing Integration
        - Sales Integration
    """,
    'author': 'IT Plus',
    'depends': [
        'base',
        'sale',
        'sale_management',
        'mrp',
        'stock'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/daily_bom_sequence.xml',
        'views/action_approve_tree_view.xml',
        'views/action_approve_view.xml',
        'views/daily_bom_views.xml',
        'views/mrp_production_view.xml',
        'views/quality_measure_views.xml',
        'views/quality_test_views.xml',
        'views/stock_picking_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
