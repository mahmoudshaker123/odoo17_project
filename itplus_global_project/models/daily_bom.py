from odoo import _, models, fields, api
from odoo.exceptions import ValidationError

class DailyBOM(models.Model):
    _name = 'daily.bom'
    _description = 'Daily Bill of Materials'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string="Reference", required=True, copy=False, readonly=True,
                       default=lambda self: _('New'))

    date = fields.Date(string="Date", default=fields.Date.context_today)
    product_id = fields.Many2one('product.product', string="Finished Product", required=True)
    sale_order_id = fields.Many2one('sale.order', string="Related Sale Order")
    product_count = fields.Integer(string="Quantity")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed')
    ], default='draft', tracking=True)

    line_ids = fields.One2many('daily.bom.line', 'bom_id', string="Raw Materials")

    @api.onchange('product_id')
    def _onchange_product_id_prefill_components(self):
        """When selecting a finished product, prefill raw materials from its BoM.
        Always replace existing lines when product changes.
        """
        if not self.product_id:
            self.line_ids = [(5, 0, 0)]  # تفريغ أي خطوط موجودة
            return

        # مسح أي خطوط قديمة قبل التحديث
        self.line_ids = [(5, 0, 0)]

        # البحث عن BoM للمنتج
        bom = self.env['mrp.bom'].search([
            ('product_tmpl_id', '=', self.product_id.product_tmpl_id.id),
            ('active', '=', True)
        ], limit=1)

        if not bom:
            return

        new_lines = []
        for bom_line in bom.bom_line_ids:
            new_lines.append((0, 0, {
                'product_id': bom_line.product_id.id,
                'quantity': bom_line.product_qty,
            }))

        if new_lines:
            self.line_ids = new_lines

    def action_confirm(self):
        for rec in self:
            if not rec.line_ids:
                raise ValidationError("You must add at least one material.")

            rec.state = 'confirmed'
            
            # تحقق من تأكيد Sale Order إذا كان مرتبط
            if rec.sale_order_id:
                # تحقق إذا كل الـ Daily BOMs المرتبطة بهذا Sale Order تم تأكيدها
                all_daily_boms = self.env['daily.bom'].search([
                    ('sale_order_id', '=', rec.sale_order_id.id)
                ])
                all_confirmed = all(bom.state == 'confirmed' for bom in all_daily_boms)
                
                # إذا كل الـ Daily BOMs تم تأكيدها، أكد الـ Sale Order
                if all_confirmed and rec.sale_order_id.state in ('draft', 'sent'):
                    rec.sale_order_id.action_confirm()
                    
                    # فتح الـ Sale Order بعد التأكيد
                    return {
                        'type': 'ir.actions.act_window',
                        'name': _('Sale Order'),
                        'res_model': 'sale.order',
                        'view_mode': 'form',
                        'res_id': rec.sale_order_id.id,
                        'target': 'current',
                    }

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('daily.bom') or _('New')
        return super().create(vals)


class DailyBOMLine(models.Model):
    _name = 'daily.bom.line'
    _description = 'Daily BOM Line'

    bom_id = fields.Many2one('daily.bom', string="Daily BOM", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Raw Material", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure", related='product_id.uom_id', readonly=True)