from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    manufacturing_ids = fields.One2many('mrp.production', 'sale_line_id', string="Related MOs")

    item_ids = fields.One2many(
        'sale.item',
        'sale_order_line_id',
        string='Items'
    )

    total_items_amount = fields.Float(string="Total Items", compute="_compute_total_items", store=True)

    @api.depends('item_ids.total')
    def _compute_total_items(self):
        for line in self:
            line.total_items_amount = sum(item.total for item in line.item_ids)

    def action_open_item_wizard(self):
        return {
            'name': 'Add Items',
            'type': 'ir.actions.act_window',
            'res_model': 'add.sale.item.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_line_id': self.id,
            }
        }

