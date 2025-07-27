from odoo import models, fields, api

class SaleItem(models.Model):
    _name = 'sale.item'
    _description = 'Sale Item'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    length = fields.Float(string="Length")
    quantity = fields.Float(string="Quantity")
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends('length', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.length * rec.quantity
