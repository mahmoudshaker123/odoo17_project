from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string="Approval Status", tracking=True)

    def action_approve(self):
        DailyBOM = self.env['daily.bom']
        for order in self:

            for line in order.order_line:
                # Create Daily BOM
                daily_bom = DailyBOM.create({
                    'product_id': line.product_id.id,
                    'sale_order_id': order.id,
                    'product_count': line.product_uom_qty,
                })
                # ممكن تضيف خامات مبدئية هنا لو حابب
                order.approval_state = 'approved'

        return {
            'type': 'ir.actions.act_window',
            'name': 'Daily BOMs',
            'res_model': 'daily.bom',
            'view_mode': 'tree,form',
            'target': 'current',
            'domain': [('sale_order_id', '=', self.id)],
        }

    def action_reject(self):
        for order in self:
            order.approval_state = 'rejected'
