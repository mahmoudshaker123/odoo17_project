from datetime import date
from odoo import models ,fields , api


class HmsPatient(models.Model):
    _name = 'hms.patient'

    first_name= fields.Char(required=True)
    last_name= fields.Char(required=True)
    department_id = fields.Many2one('hms.department')
    department_capacity = fields.Integer(related="department_id.capacity")
    doctor_ids= fields.Many2many('hms.doctor')
    state = fields.Selection([
        ('undetermined','Undetermined'),
        ('good','Good'),
        ('fair','Fair'),
        ('serious','Serious'),
    ],
     default='undetermined')
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


    @api.onchange('age')
    def _onchange_check_pcr(self):
        if self.age < 30 :
            self.pcr = True
            return {
                'warning':{
                    'title':"PCR Checked",
                    'message':" PCR has been checked automatically because age is below 30",
                }
            }

    @api.onchange('birth_date')
    def _onchange_age(self):
        if self.birth_date :
            today = date.today()
            self.age = today.year - self.birth_date.year


    @api.onchange('department_id')
    def _onchange_department_id(self):
        if not self.department_id:
            self.doctor_ids=False

