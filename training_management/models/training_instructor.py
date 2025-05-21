from  odoo import  fields , models

class TrainingInstructor(models.Model):
    _name = 'training.instructor'

    name = fields.Char(required=True)
    specialization = fields.Char()
    phone = fields.Char()
    image = fields.Image()
