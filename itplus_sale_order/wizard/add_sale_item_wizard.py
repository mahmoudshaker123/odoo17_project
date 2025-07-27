from odoo import models, fields, api

class AddSaleItemWizard(models.TransientModel):
    _name = 'add.sale.item.wizard'

    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line", required=True)
    product_id = fields.Many2one(related='sale_order_line_id.product_id', string="Product", readonly=True)
    item_ids = fields.One2many('add.sale.item.line.wizard', 'wizard_id', string="Items")

    def action_add_items(self):
        for line in self.item_ids:
            new_item = self.env['sale.item'].create({
                'length': line.length,
                'quantity': line.quantity,
                'sale_order_line_id': self.sale_order_line_id.id,
            })


class AddSaleItemLineWizard(models.TransientModel):
    _name = 'add.sale.item.line.wizard'

    wizard_id = fields.Many2one('add.sale.item.wizard', string="Wizard")
    length = fields.Float(string="Length")
    quantity = fields.Float(string="Quantity")
    total = fields.Float(string="Total", compute="_compute_total", store=True)

    @api.depends('length', 'quantity')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.length * rec.quantity
