from odoo import models , fields ,api
from odoo.tools.populate import compute


class ResPartner(models.Model):
    _inherit = 'res.partner'

    property_id = fields.Many2one('property')
    price = fields.Float(related='property_id.selling_price')
    #price = fields.Float(compute='_compute_price' , store=1)

    # @api.depends('property_id')
    # def _compute_price(self):
    #     for rec in self:
    #         rec.price=rec.property_id.selling_price


