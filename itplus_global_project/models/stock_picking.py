# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_quality_checks = fields.Boolean(
        string='Has Quality Checks',
        compute='_compute_quality_flags_and_counts',
        store=True
    )
    required_quality_checks_count = fields.Integer(
        string='Required Quality Checks',
        compute='_compute_quality_flags_and_counts',
        store=True
    )
    completed_quality_checks_count = fields.Integer(
        string='Completed Quality Checks',
        compute='_compute_quality_flags_and_counts',
        store=True
    )
    quality_test_ids = fields.One2many(
        'quality.test',
        'picking_id',
        string="Quality Tests"
    )

    @api.depends('move_ids', 'move_ids.product_id', 'location_id', 'location_dest_id')
    def _compute_quality_flags_and_counts(self):
        """يحسب هل في فحوصات جودة مطلوبة وعدد المطلوب والمكتمل (passed)."""
        QualityMeasure = self.env['quality.measure']
        QualityTest = self.env['quality.test']

        for picking in self:
            required_measure_ids_set = set()
            for move in picking.move_ids:
                if not move.product_id:
                    continue
                measures = QualityMeasure.search([
                    ('product_id', '=', move.product_id.id),
                    ('location_id', 'in', [picking.location_id.id, picking.location_dest_id.id]),
                    ('active', '=', True),
                ])
                required_measure_ids_set.update(measures.ids)

            picking.has_quality_checks = bool(required_measure_ids_set)
            picking.required_quality_checks_count = len(required_measure_ids_set)

            if not required_measure_ids_set:
                picking.completed_quality_checks_count = 0
                continue

            # جِب كل الـ Tests اللي Passed
            passed_tests = QualityTest.search([
                ('quality_measure_id', 'in', list(required_measure_ids_set)),
                ('test_status', '=', 'pass'),
                ('picking_id', '=', picking.id),
            ])
            passed_measure_ids = set(passed_tests.mapped('quality_measure_id').ids)

            picking.completed_quality_checks_count = len(passed_measure_ids & required_measure_ids_set)

    def button_validate(self):
        for picking in self:
            for move in picking.move_ids_without_package:
                product = move.product_id

                # ندور على أي test خاص بالمنتج والمخزن (اختبارات عامة)
                quality_tests = self.env['quality.test'].search([
                    ('product_id', '=', product.id),
                    ('picking_id', '=', False),  # اختبارات عامة فقط
                    ('location_id', 'in', [picking.location_id.id, picking.location_dest_id.id])
                ])

                # لو مفيش أي test → عادي نعمل validate
                if not quality_tests:
                    continue

                # لو فيه tests → لازم كلها تكون Passed
                failed_tests = quality_tests.filtered(lambda t: t.test_status != 'pass')
                if failed_tests:
                    raise UserError(_(
                        "Cannot validate this transfer.\n"
                        "Product: %s\n"
                        "Location: %s\n"
                        "Measure/Test: %s\n"
                        "Status: %s"
                    ) % (
                        product.display_name,
                        picking.location_id.display_name,
                        ", ".join(failed_tests.mapped("quality_measure_id.name")),
                        ", ".join(failed_tests.mapped("test_status"))
                    ))

        return super(StockPicking, self).button_validate()

    def action_view_quality_tests(self):
        """يفتح نافذة الـ Quality Tests للمنتجات في هذا التحويل."""
        self.ensure_one()
        action = self.env.ref('itplus_global_project.action_quality_test').read()[0]
        # عرض الاختبارات العامة للمنتجات في هذا التحويل
        product_ids = self.move_ids.mapped('product_id').ids
        action['domain'] = [
            ('product_id', 'in', product_ids),
            ('picking_id', '=', False)  # اختبارات عامة فقط
        ]
        action['context'] = {
            'default_product_id': self.move_ids[0].product_id.id if self.move_ids else False,
        }
        return action
