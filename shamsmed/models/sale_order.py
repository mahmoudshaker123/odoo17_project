# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    approval_state = fields.Selection([
        ('draft', 'Draft'),
        ('to_manager', 'To Manager'),
        ('manager_rejected', 'Manager Rejected'),
        ('to_supervisor', 'To Supervisor'),
        ('supervisor_rejected', 'Supervisor Rejected'),
        ('approved', 'Approved'),
    ], string='Approval State', default='draft', tracking=True)

    rejection_history_ids = fields.One2many(
        'sale.rejection.history',
        'sale_order_id',
        string='Rejection History'
    )

    def action_submit_to_manager(self):
        self.ensure_one()
        if self.approval_state != 'draft':
            raise UserError(_('Only draft quotations can be submitted.'))
        self.approval_state = 'to_manager'

    def action_manager_approve(self):
        self.ensure_one()
        if self.approval_state != 'to_manager':
            raise UserError(_('Only quotations pending manager approval can be approved.'))
        self.approval_state = 'to_supervisor'

    def action_manager_reject(self):
        self.ensure_one()
        if self.approval_state != 'to_manager':
            raise UserError(_('Only quotations pending manager approval can be rejected.'))

        # المسؤول السابق هو المندوب
        previous_user = self.user_id

        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Quotation'),
            'res_model': 'sale.order.rejection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
                'default_rejected_by': self.env.user.id,
                'default_rejected_to': previous_user.id,
                'default_state_from': 'to_manager',
                'default_state_to': 'manager_rejected',
            }
        }

    def action_supervisor_approve(self):
        self.ensure_one()
        if self.approval_state != 'to_supervisor':
            raise UserError(_('Only quotations pending supervisor approval can be approved.'))
        self.approval_state = 'approved'

    def action_supervisor_reject(self):
        self.ensure_one()
        if self.approval_state != 'to_supervisor':
            raise UserError(_('Only quotations pending supervisor approval can be rejected.'))

        # المسؤول السابق هو المدير (آخر من أخذ المرحلة)
        last_rejection = self.rejection_history_ids.sorted(lambda r: (r.date, r.time), reverse=True)[:1]
        if last_rejection:
            previous_user = last_rejection[0].to_user_id
        else:
            previous_user = self.env.user

        return {
            'type': 'ir.actions.act_window',
            'name': _('Reject Quotation'),
            'res_model': 'sale.order.rejection.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_sale_order_id': self.id,
                'default_rejected_by': self.env.user.id,
                'default_rejected_to': previous_user.id,
                'default_state_from': 'to_supervisor',
                'default_state_to': 'supervisor_rejected',
            }
        }

    def action_resubmit(self):
        self.ensure_one()
        if self.approval_state not in ['manager_rejected', 'supervisor_rejected']:
            raise UserError(_('Only rejected quotations can be resubmitted.'))

        last_rejection = self.rejection_history_ids.sorted(lambda r: (r.date, r.time), reverse=True)[:1]
        if not last_rejection:
            raise UserError(_('No rejection history found.'))

        last_rejection = last_rejection[0]

        # المستخدم الحالي لازم يكون المسؤول السابق
        if self.env.user != last_rejection.previous_state_user_id:
            raise UserError(_('Only the previous responsible user can resubmit this quotation.'))

        # إعادة الحالة للمرحلة السابقة
        if self.approval_state == 'manager_rejected':
            self.approval_state = 'draft'
        elif self.approval_state == 'supervisor_rejected':
            self.approval_state = 'to_manager'

    def _create_rejection_history(self, state_from, state_to, reason, rejected_by, rejected_to):
        self.ensure_one()

        # المسؤول السابق يعتمد على نوع الرفض
        if state_to == 'manager_rejected':
            previous_user = self.user_id  # المندوب
        elif state_to == 'supervisor_rejected':
            # المسؤول السابق هو آخر من أخذ المرحلة "to_manager" → المدير
            previous_user = self.env['res.users'].search(
                [('groups_id', 'in', self.env.ref('shamsmed.group_sales_manager').id)],
                limit=1
            )
        else:
            previous_user = rejected_to

        self.env['sale.rejection.history'].create({
            'sale_order_id': self.id,
            'from_user_id': rejected_by.id,
            'to_user_id': rejected_to.id,
            'reason': reason,
            'state_from': state_from,
            'state_to': state_to,
            'previous_state_user_id': previous_user.id,
        })

    def action_confirm(self):
        for order in self:
            # تأكيد لازم يكون بعد موافقة المدير + المشرف
            if order.approval_state != 'approved':
                raise UserError(
                    _("You cannot confirm this quotation until it has been approved by all levels (salesperson, manager, and supervisor)."))
        return super(SaleOrder, self).action_confirm()
