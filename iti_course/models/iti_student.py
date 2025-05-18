from dateutil.utils import today

from odoo import fields , models , api
from datetime import date

class ItiStudent(models.Model):
    _name = 'iti.student'

    name=fields.Char(required=True)
    email=fields.Char()
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
    state = fields.Selection([
        ('applied','Applied'),
        ('first','First Interview'),
        ('second','Second Interview'),
        ('passed', 'Passed'),
        ('rejected','Rejected'),
    ],
        default='applied'
    )

    @api.model
    def create(self, vals):
        name_split = vals['name'].split()
        vals['email']= f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().create(vals)

    def write(self, vals):
        name_split = vals['name'].split()
        vals['email'] = f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().write(vals)

    def set_first_action(self):
        for rec in self:
            rec.state = 'first'

    def set_second_action(self):
        for rec in self:
            rec.state = 'second'

    def set_passed_action(self):
        for rec in self:
            rec.state = 'passed'

    def set_rejected_action(self):
        for rec in self:
            rec.state = 'rejected'

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

