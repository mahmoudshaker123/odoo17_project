from odoo import models, fields ,api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    delivery_order_id = fields.Many2one(
       'stock.picking',
        string='Delivery Order',

    )

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            delivery_order = self.env['stock.picking'].search([('sale_id', '=', order.id)], limit=1)
            if delivery_order:
                order.delivery_order_id = delivery_order.id
        return res

