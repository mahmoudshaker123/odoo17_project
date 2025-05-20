from  odoo import fields , models


class TrainingCourse(models.Model):
    _name = 'training.course'

    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Date()
    duration = fields.Integer()
    instructor_id = fields.Many2one('training.instructor')