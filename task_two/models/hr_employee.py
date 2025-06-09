from odoo import fields , models ,api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number=fields.Integer(string='Employee Number')

    _sql_constraints = [
        ('unique_employee_number', 'unique("employee_number")', 'This employee number is exist')
    ]





