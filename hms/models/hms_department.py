from odoo import  fields , models


class HmsDepartment(models.Model):
    _name = 'hms.department'

    name=fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patient_ids= fields.One2many('hms.patient' ,'department_id')
