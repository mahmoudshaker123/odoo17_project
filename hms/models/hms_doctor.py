from odoo import fields, models


class HmsDoctor(models.Model):
    _name = 'hms.doctor'

    first_name = fields.Char()
    last_name = fields.Char()
    image = fields.Image()
    patient_ids = fields.Many2many('hms.patient')


