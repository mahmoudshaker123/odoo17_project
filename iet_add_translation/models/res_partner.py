from odoo import fields , models ,api


class AddTranslation(models.Model):
    _inherit = 'res.partner'

    name_ar = fields.Char(string="Arabic Name")
    street1_ar = fields.Char(string="Street 1 AR")
    street2_ar = fields.Char(string="Street 2 AR")
    city_ar = fields.Char(string="City AR")
    state_ar = fields.Char(string="State AR")
    country_ar = fields.Char(string="Country AR")
