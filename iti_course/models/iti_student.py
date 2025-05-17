from dateutil.utils import today

from odoo import fields , models , api
from datetime import date

class ItiStudent(models.Model):
    _name = 'iti.student'

    name=fields.Char(required=True)
    birth_date=fields.Date()
    age = fields.Integer(string="Age")
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
    track_id = fields.Many2one('iti.track')
    track_capacity = fields.Integer(related="track_id.capacity")
    skill_ids= fields.Many2many('iti.skill')
    grade_ids = fields.One2many('student.course.line' ,'student_id')

    @api.onchange("gender")
    def _onchange_gender(self):
        if self.gender == 'male':
            self.salary = 10000
        else:
            self.salary = 8000


    @api.onchange("birth_date")
    def _onchange_birth_date(self):
        if self.birth_date:
            today = date.today()
            self.age = today.year - self.birth_date.year


class ItiCourse(models.Model):
    _name = 'iti.course'

    name=fields.Char()



class StudentCourseGrades(models.Model):
    _name = 'student.course.line'

    student_id= fields.Many2one('iti.student')
    course_id= fields.Many2one('iti.course')
    grade = fields.Selection([
        ('good','Good'),
        ('very_good','Very Good'),
    ])