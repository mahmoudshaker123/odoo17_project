from  odoo import  fields , models


class TrainingStudent(models.Model):
    _name = 'training.student'

    name=fields.Char()
    email=fields.Char()
    phone=fields.Char()
    course_ids = fields.Many2many(
                    'training.course',
                         'training_course_student_rel',
                        'student_id',
                        'course_id',
                        string="Courses"
                    )
