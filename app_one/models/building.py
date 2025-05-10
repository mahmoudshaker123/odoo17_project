from email.policy import default

from odoo import models , fields


class Building(models.Model):
    _name = 'building'
    _inherit =['mail.thread','mail.activity.mixin']
    _description = 'Building Record'

    no = fields.Integer()
    name = fields.Char()
    code = fields.Char()
    description = fields.Text()
    active= fields.Boolean(default=True)


