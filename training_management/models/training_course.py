from  odoo import fields , models,api


class TrainingCourse(models.Model):
    _name = 'training.course'

    name = fields.Char(required=True)
    description = fields.Text()
    date = fields.Date()
    duration = fields.Integer()
    instructor_id = fields.Many2one('training.instructor')
    student_ids = fields.Many2many(
        'training.student',
        'training_course_student_rel',
        'course_id',
        'student_id',
        string="Students"
    )


