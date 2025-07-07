from odoo import models, api, _
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model_create_multi
    def create(self, vals_list):
        if not self.env.user.has_group('iet_add_permission.group_customer_creation'):
            raise ValidationError(_("You do not have permission to create customers."))
        return super().create(vals_list)

    def unlink(self):
        if not self.env.user.has_group('iet_add_permission.group_customer_creation'):
            raise ValidationError(_("You do not have permission to delete customers."))
        return super().unlink()

    def write(self, vals):
        if 'active' in vals or 'name' in vals or 'email' in vals:
            if not self.env.user.has_group('iet_add_permission.group_customer_creation'):
                raise ValidationError(_("You do not have permission to archived customers."))
        return super().write(vals)

    def export_data(self, fields_to_export):
        if not self.env.user.has_group('iet_add_permission.group_customer_creation'):
            raise ValidationError(_("You do not have permission to export customers."))
        return super().export_data(fields_to_export)
