from odoo import models, api, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def export_data(self, fields_to_export, raw_data=False):
        if not self.env.user.has_group('iet_add_permission.group_product_creation'):
            raise ValidationError(_("You do not have permission to export products."))
        return super().export_data(fields_to_export, raw_data=raw_data)

    def _check_user_permission(self):
        if not self.env.user.has_group('iet_add_permission.group_product_creation'):
            raise ValidationError(_("You do not have permission to perform this action on products."))

    def unlink(self):
        self._check_user_permission()
        return super().unlink()

    def write(self, vals):
        self._check_user_permission()
        return super().write(vals)

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group('iet_add_permission.group_product_creation'):
            raise ValidationError(_("You do not have permission to create products."))
        return super().create(vals_list)
