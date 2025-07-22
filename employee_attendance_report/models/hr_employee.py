from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'



    def action_open_attendance_report_wizard(self):
        action = self.env['ir.actions.actions']._for_xml_id('employee_attendance_report.attendance_report_wizard_action')
        action['context'] = {'default_employee_id': self.id}
        return action
