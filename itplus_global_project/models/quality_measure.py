# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class QualityMeasure(models.Model):
    _name = 'quality.measure'
    _description = 'Quality Measure'
    _order = "id desc"

    name = fields.Char('Name', required=True)
    product_id = fields.Many2one('product.product', string='Product', required=True)
    location_id = fields.Many2one('stock.location', string="Stock Location", required=True)
    
    type = fields.Selection([
        ('quantity', 'Quantitative'),
        ('quality', 'Qualitative')
    ], string='Test Type', default='quantity', required=True)
    
    quantity_min = fields.Float('Min Value')
    quantity_max = fields.Float('Max Value')
    active = fields.Boolean('Active', default=True)

    @api.constrains('type', 'quantity_min', 'quantity_max')
    def _check_limits(self):
        for rec in self:
            if rec.type == 'quantity':
                if rec.quantity_min is None or rec.quantity_max is None:
                    raise models.ValidationError(_("Please set Min/Max for quantitative measures."))
                if rec.quantity_min > rec.quantity_max:
                    raise models.ValidationError(_("Min value cannot be greater than Max value."))

    def evaluate_value(self, numeric_value=None, qualitative_value=None):
        self.ensure_one()
        if self.type == 'quantity':
            if numeric_value is None:
                return 'fail'
            return 'pass' if self.quantity_min <= numeric_value <= self.quantity_max else 'fail'
        return 'pass' if qualitative_value == 'satisfied' else 'fail'
