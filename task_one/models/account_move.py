from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_order_id = fields.Many2one(
        'stock.picking',
        string='Delivery Order',
    )

    @api.model
    def create(self, vals):
        move = super().create(vals)
        if not move.delivery_order_id and move.invoice_origin:
            sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
            if sale_order and sale_order.delivery_order_id:
                move.delivery_order_id = sale_order.delivery_order_id.id
        return move
