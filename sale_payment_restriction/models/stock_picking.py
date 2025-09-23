from odoo import models, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = "stock.picking"

    def button_validate(self):
        for picking in self:
            if picking.sale_id:
                sale = picking.sale_id
                if sale.x_paid_amount < sale.amount_total:
                    raise UserError(_("You cannot validate this delivery because the customer has not paid the full amount."))
        return super(StockPicking, self).button_validate()
