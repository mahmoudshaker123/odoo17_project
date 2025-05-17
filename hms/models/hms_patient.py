from odoo import models ,fields


class Hms(models.Model):
    _name = 'hms.patient'

    first_name= fields.Char()
    last_name= fields.Char()
    birth_date=fields.Date()
    history=fields.Html()
    cr_ratio= fields.Float()
    blood_type=fields.Selection([
        ('a+', 'A+'),
        ('a-', 'A-'),
        ('b+', 'B+'),
        ('b-', 'B-'),
        ('ab+', 'AB+'),
        ('ab-', 'AB-'),
        ('o+', 'O+'),
        ('o-', 'O-'),
    ], string="Blood Type")

    pcr = fields.Boolean()
    image = fields.Image()
    address = fields.Text()
    age= fields.Integer()
