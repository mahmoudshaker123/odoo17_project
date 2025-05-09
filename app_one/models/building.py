
from odoo import models , fields


class Building(models.Model):
    _name = 'building'
    _inherit =['mail.thread','mail.activity.mixin']
    _description = 'Building Record'

    no = fields.Integer()
    code = fields.Char()
    description = fields.Text()

