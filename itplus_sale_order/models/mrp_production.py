from odoo import models, fields

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    sale_id = fields.Many2one('sale.order', string="Sale Order")
    sale_line_id = fields.Many2one('sale.order.line', string="Related Sale Order Line")


