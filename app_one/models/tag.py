from odoo import models , fields



class Tag(models.Model):
    _name = 'tag'
    _description = 'Tag model'

    name = fields.Char(required=1 )