# wizards/attendance_report_wizard.py
from odoo import models, fields

class AttendanceReportWizard(models.TransientModel):
    _name = 'attendance.report.wizard'
    _description = 'Attendance Report Wizard'

    employee_id = fields.Many2one('hr.employee', required=True, readonly=True)
    start_date = fields.Date(required=True)
    end_date = fields.Date(required=True)

    def action_generate_report(self):
        return self.env.ref('employee_attendance_report.action_attendance_pdf_report').report_action(self)
