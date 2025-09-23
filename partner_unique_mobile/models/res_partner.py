from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    _sql_constraints = [
        ('unique_mobile', 'unique(mobile)', 'رقم الموبايل موجود بالفعل!'),
    ]
