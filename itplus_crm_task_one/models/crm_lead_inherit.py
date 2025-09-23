from odoo import fields , models


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    source_type = fields.Selection([
        ('1','عميل ادارة'),
        ('2','اعلان ممول'),
        ('3','اضافة من الموظفين او جهات الاتصال'),
    ]
        , string='مصدر العميل')