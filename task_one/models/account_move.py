from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    delivery_order_id = fields.Many2one(
        'stock.picking',
        string='Delivery Order',
        compute='_compute_delivery_order',
        store=True,
        readonly=True
    )

    @api.depends('invoice_origin')
    def _compute_delivery_order(self):
        for move in self:
            if move.invoice_origin:
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order:
                    picking = self.env['stock.picking'].search([('sale_id', '=', sale_order.id)], limit=1)
                    move.delivery_order_id = picking.id if picking else False
            else:
                move.delivery_order_id = False