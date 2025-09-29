# -*- coding: utf-8 -*-
{
    'name': 'Sales Approval Workflow',
    'version': '17.0.1.0.0',
    'category': 'Sales',
    'summary': 'Custom approval workflow for sales quotations',
    'description': """
        Sales Approval Workflow
        ======================
        
        This module extends the Sales application with a custom approval workflow for quotations.
        
        Features:
        - 4-level approval workflow (Representative → Manager → Supervisor → Approved)
        - Rejection notes with privacy controls
        - Role-based access control
        - Custom states and buttons
    """,
    'author': 'Mahmoud shaker',
    'depends': ['base', 'sale', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/sale_rejection_history_views.xml',
        'views/sale_order_views.xml',
        'wizard/rejection_wizard_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
}
