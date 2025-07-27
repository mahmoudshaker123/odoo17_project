from odoo import models, fields, api, _
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    manufacturing_ids = fields.One2many('mrp.production', 'sale_id', string="Manufacturing Orders")

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            mo_created = False
            for line in order.order_line:
                if line.total_items_amount > 0:
                    mo = self.env['mrp.production'].create({
                        'product_id': line.product_id.id,
                        'product_qty': line.total_items_amount,
                        'sale_line_id': line.id,
                        'product_uom_id': line.product_uom.id,
                        'origin': order.name,
                        'sale_id': order.id,
                    })
                    mo_created = True
            if mo_created:
                return {
                    'effect': {
                        'fadeout': 'slow',
                        'message': _('Manufacturing Orders Created Successfully!'),
                        'type': 'rainbow_man',
                    }
                }
        return res
