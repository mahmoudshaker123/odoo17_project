# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class QualityTest(models.Model):
    _name = 'quality.test'
    _description = 'Quality Test'
    _order = "id desc"

    # معلومات أساسية
    name = fields.Char('Test Name', required=True)
    description = fields.Text('Description')
    
    # ربط بالمعيار والمنتج والمخزن
    quality_measure_id = fields.Many2one('quality.measure', string='Quality Measure', required=True)
    product_id = fields.Many2one(related='quality_measure_id.product_id', store=True, readonly=True)
    location_id = fields.Many2one(related='quality_measure_id.location_id', store=True, readonly=True)
    test_type = fields.Selection(related='quality_measure_id.type', store=True, readonly=True)
    
    # نتائج الفحص
    test_result = fields.Float(string='Numeric Result')
    test_result2 = fields.Selection([
        ('satisfied', 'Satisfied'),
        ('unsatisfied', 'Unsatisfied')
    ], string='Qualitative Result')
    
    # حالة الفحص
    test_status = fields.Selection([
        ('draft', 'Draft'),
        ('pass', 'Passed'),
        ('fail', 'Failed')
    ], string='Status', default='draft', required=True)
    
    # معلومات إضافية
    picking_id = fields.Many2one('stock.picking', string="Stock Operation", required=False)
    test_date = fields.Datetime('Test Date', default=fields.Datetime.now)
    tested_by = fields.Many2one('res.users', string='Tested By', default=lambda self: self.env.user)
    notes = fields.Text('Notes')
    
    # حقول محسوبة
    is_passed = fields.Boolean('Is Passed', compute='_compute_is_passed', store=True)
    
    @api.depends('test_result', 'test_result2', 'quality_measure_id', 'test_type')
    def _compute_quality_test_status(self):
        """تقييم حالة الفحص بناءً على المعيار"""
        for test in self:
            if test.quality_measure_id and test.test_type:
                if test.test_type == 'quantity' and test.test_result is not None:
                    result = test.quality_measure_id.evaluate_value(numeric_value=test.test_result)
                    test.test_status = result
                elif test.test_type == 'quality' and test.test_result2:
                    result = test.quality_measure_id.evaluate_value(qualitative_value=test.test_result2)
                    test.test_status = result
    
    @api.depends('test_status')
    def _compute_is_passed(self):
        """حقل محسوب لسهولة الفلترة"""
        for test in self:
            test.is_passed = (test.test_status == 'pass')
    
    def action_pass(self):
        """إجراء تمرير الفحص"""
        self.write({'test_status': 'pass'})
    
    def action_fail(self):
        """إجراء فشل الفحص"""
        self.write({'test_status': 'fail'})
    
    def action_reset(self):
        """إعادة تعيين الفحص"""
        self.write({'test_status': 'draft'})
    
    @api.onchange('test_result', 'test_result2')
    def _onchange_test_results(self):
        """تحديث تلقائي للحالة عند تغيير النتائج"""
        if self.quality_measure_id:
            self._compute_quality_test_status()
