from odoo import models, fields, api

class JobOrder(models.Model):
    _name = 'job.order'
    _description = 'Job Order'

    sequence = fields.Char(default='New', readonly=True, string='Sequence', copy=False)
    responsible = fields.Many2one(
        'res.users',
        string="Responsible",
        domain="[('share', '=', False)]",
        required=1
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
    ],
        default='draft'
    )
    date = fields.Datetime(default=fields.Datetime.now, required=True, string='Date')

    bom_line_ids = fields.One2many('job.order.line', 'job_order_id', string='BOM Lines')




    def action_draft(self):
        for rec in self:
            rec.state= 'draft'

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'
            for line in rec.bom_line_ids:
                mo = self.env['mrp.production'].create({
                    'product_id': line.bill_of_material.product_tmpl_id.id,
                    'product_qty': line.quantity,
                    'bom_id': line.bill_of_material.id,
                    'user_id': rec.responsible.id,
                })
                mo.action_confirm()

    @api.model
    def create(self, vals):
        res = super(JobOrder, self).create(vals)
        if res.sequence == 'New':
            res.sequence = self.env['ir.sequence'].next_by_code('job_order_seq')
        return res

    def action_open_related_manufacturing_orders(self):
        action = self.env['ir.actions.actions']._for_xml_id('mrp.mrp_production_action')
        return action


class JobOrderLine(models.Model):
    _name = 'job.order.line'
    _description = 'Job Order BOM Line'

    job_order_id = fields.Many2one('job.order', string='Job Order', required=True, ondelete='cascade')
    bill_of_material = fields.Many2one('mrp.bom', string='Bill of Material', required=True)
    quantity = fields.Float(string='Quantity', default=1.0)
