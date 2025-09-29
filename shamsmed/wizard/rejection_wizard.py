# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrderRejectionWizard(models.TransientModel):
    _name = 'sale.order.rejection.wizard'
    _description = 'Sale Order Rejection Wizard'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Sale Order',
        required=True
    )
    rejected_by = fields.Many2one(
        'res.users',
        string='Rejected By',
        required=True,
        default=lambda self: self.env.user
    )
    rejected_to = fields.Many2one(
        'res.users',
        string='Rejected To',
        required=True,
        default=lambda self: self._context.get('default_rejected_to')
    )

    reason = fields.Text(
        string='Rejection Reason',
        required=True,
        help='Please provide a detailed reason for rejecting this quotation.'
    )
    state_from = fields.Selection([
        ('draft', 'Draft'),
        ('to_manager', 'To Manager'),
        ('manager_rejected', 'Manager Rejected'),
        ('to_supervisor', 'To Supervisor'),
        ('supervisor_rejected', 'Supervisor Rejected'),
        ('approved', 'Approved'),
    ], string='State From', required=True)
    state_to = fields.Selection([
        ('draft', 'Draft'),
        ('manager_rejected', 'Manager Rejected'),
        ('to_supervisor', 'To Supervisor'),
        ('supervisor_rejected', 'Supervisor Rejected'),
        ('approved', 'Approved'),
    ], string='State To', required=True)

    def action_reject(self):
        self.ensure_one()

        # إنشاء سجل في الـ History
        self.sale_order_id._create_rejection_history(
            self.state_from,
            self.state_to,
            self.reason,
            self.rejected_by,
            self.rejected_to
        )

        # تحديث حالة الـ Sale Order
        self.sale_order_id.approval_state = self.state_to

        # إنشاء نشاط للشخص المسؤول عن الإجراء
        self.sale_order_id.activity_schedule(
            'mail.mail_activity_data_todo',
            summary=_('Quotation Rejected - Action Required'),
            note=_('Quotation %s has been rejected. Reason: %s') % (self.sale_order_id.name, self.reason),
            user_id=self.rejected_to.id
        )

        return {'type': 'ir.actions.act_window_close'}

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        sale_order = False

        if self.env.context.get('active_model') == 'sale.order' and self.env.context.get('active_id'):
            sale_order = self.env['sale.order'].browse(self.env.context['active_id'])
            res['sale_order_id'] = sale_order.id

        if sale_order and sale_order.approval_state in ['to_manager', 'to_supervisor']:
            if sale_order.approval_state == 'to_manager':
                # بيرجع للمندوب
                res['rejected_to'] = sale_order.user_id.id
            elif sale_order.approval_state == 'to_supervisor':
                # بيرجع للمدير
                manager_group = self.env.ref('shamsmed.group_sales_manager')
                manager_user = self.env['res.users'].search(
                    [('groups_id', 'in', [manager_group.id])],
                    limit=1
                )
                if manager_user:
                    res['rejected_to'] = manager_user.id

        return res
