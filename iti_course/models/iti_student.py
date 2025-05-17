from odoo import fields , models

class ItiStudent(models.Model):
    _name = 'iti.student'

    name=fields.Char()
    birth_date=fields.Date()
    salary=fields.Float()
    address = fields.Text()
    gender = fields.Selection([
        ('male','Male'),
        ('female','Female'),
    ])
    accepted = fields.Boolean()
    level = fields.Integer()
    image=fields.Binary()
    cv = fields.Html()
    login_time = fields.Datetime()