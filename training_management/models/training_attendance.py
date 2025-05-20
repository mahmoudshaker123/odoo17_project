from odoo import fields , models

class TrainingAttendance(models.Model):
    _name = 'training.attendance'

    student_id = fields.Many2one('training.student' , required=True)
    course_id = fields.Many2one('training.course' , required=True)
    date = fields.Date(default =fields.Date.today)
    state = fields.Selection([
        ('present','Present'),
        ('absent','Absent'),
    ],
        required=True
    )
