{
    "name": "Customer Metrics Dashboard",
    "summary": "Dashboard: Top 5 customers by total sales and order count",
    "version": "17.0.1.0.0",
    "author": "Mahmoud Shaker",
    "category": "sale_management",
    "license": "LGPL-3",
    "depends": ["sale"],
    "data": [
        "security/ir.model.access.csv",
        "views/menuitems.xml",
        "views/customer_metrics_views.xml",
        "data/ir_cron.xml",
    ],
    "installable": True,
    "application": True,
}
