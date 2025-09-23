from odoo import fields , models ,api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    x_paid_amount = fields.Float(string="Amount Paid")

    def action_confirm(self):
        for order in self :
            total = order.amount_total
            paid = order.x_paid_amount
            user = self.env.user

            if paid <(0.5*total) and not user.has_group("sale_payment_restriction.group_sale_payment_manager"):
                raise UserError(_("You cannot confirm this order because paid amount is less than 50% of total. Please ask a manager to confirm."))

        return super(SaleOrder,self).action_confirm()