from odoo import fields , models , api



class ItiHr(models.Model):
    _inherit ='hr.employee'

    military_certificate = fields.Binary()

