from odoo import models, fields, api
from odoo.exceptions import ValidationError
from io import BytesIO
import base64
import xlsxwriter
from datetime import datetime


class TaskReportWizard(models.TransientModel):
    _name = 'task.report.wizard'
    _description = 'Task Report Wizard'

    date_from = fields.Date(required=True)
    date_to = fields.Date(required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string="State")
    employee_ids = fields.Many2many('hr.employee', string="Employees")

    def action_generate_excel(self):
        # Prepare domain
        domain = [
            ('date', '>=', self.date_from),
            ('date', '<=', self.date_to),
        ]
        if self.state:
            domain.append(('state', '=', self.state))
        if self.employee_ids:
            domain.append(('employee', 'in', self.employee_ids.ids))

        # Fetch tasks
        tasks = self.env['task.management'].search(domain, order='employee, date')

        # Group tasks by employee
        employee_task_map = {}
        for task in tasks:
            employee = task.employee.name or 'No Employee'
            if employee not in employee_task_map:
                employee_task_map[employee] = []
            employee_task_map[employee].append(task)

        # Create Excel
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet("Task Report")

        # Styles
        bold = workbook.add_format({'bold': True})
        title_format = workbook.add_format({'bold': True, 'font_size': 14})
        header_format = workbook.add_format({'bg_color': '#D9D9D9', 'bold': True, 'border': 1})

        # Title
        title = f"Task Report from {self.date_from} to {self.date_to}"
        worksheet.write('A1', title, title_format)

        row = 3
        for employee, task_list in employee_task_map.items():
            worksheet.write(row, 0, employee, bold)
            row += 1
            worksheet.write_row(row, 0, ['Seq Number', 'Task Name', 'Date', 'Deadline', 'State'], header_format)
            row += 1
            for task in task_list:
                worksheet.write_row(row, 0, [
                    task.seq_number,
                    task.name,
                    task.date.strftime('%Y-%m-%d %H:%M') if task.date else '',
                    task.deadline.strftime('%Y-%m-%d %H:%M') if task.deadline else '',
                    task.state,
                ])
                row += 1
            row += 2  # space between employees

        workbook.close()
        output.seek(0)
        excel_data = output.read()
        output.close()

        # Download wizard
        report_name = f"Task_Report_{datetime.today().strftime('%Y%m%d_%H%M%S')}.xlsx"
        attachment = self.env['ir.attachment'].create({
            'name': report_name,
            'type': 'binary',
            'datas': base64.b64encode(excel_data),
            'res_model': 'task.report.wizard',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        download_url = f"/web/content/{attachment.id}?download=true"
        return {
            "type": "ir.actions.act_url",
            "url": download_url,
            "target": "self",
        }
