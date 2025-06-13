from odoo import http
from odoo.http import request
import io
import xlsxwriter
from datetime import datetime


class TaskExcelReport(http.Controller):

    @http.route('/task/excel/report', type='http', auth='user')
    def download_task_excel_report(self, **kwargs):
        date_from = kwargs.get('date_from')
        date_to = kwargs.get('date_to')
        state = kwargs.get('state')
        employee_id = kwargs.get('employee_id')

        domain = []

        if date_from:
            try:
                date_from_dt = datetime.strptime(date_from, "%Y-%m-%d").date()
                domain.append(('date', '>=', date_from_dt))
            except ValueError:
                return request.not_found()

        if date_to:
            try:
                date_to_dt = datetime.strptime(date_to, "%Y-%m-%d").date()
                domain.append(('date', '<=', date_to_dt))
            except ValueError:
                return request.not_found()

        if state:
            domain.append(('state', '=', state))

        if employee_id:
            try:
                domain.append(('employee', '=', int(employee_id)))
            except ValueError:
                pass

        tasks = request.env['task.management'].sudo().search(domain, order="employee asc, date asc")

        employee_tasks = {}
        for task in tasks:
            employee = task.employee.name or "No Employee"
            employee_tasks.setdefault(employee, []).append(task)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet('Tasks Report')

        # Formats
        title_format = workbook.add_format({
            'bold': True, 'font_size': 16, 'align': 'center', 'valign': 'vcenter',
            'bg_color': '#4F81BD', 'font_color': 'white'
        })
        header_format = workbook.add_format({
            'bold': True, 'bg_color': '#D3D3D3', 'border': 1, 'align': 'center', 'valign': 'vcenter'
        })
        string_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
        alt_row_format = workbook.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'bg_color': '#F9F9F9'})
        date_format = workbook.add_format({'num_format': 'yyyy-mm-dd', 'border': 1, 'align': 'center'})

        # Adjust column widths
        worksheet.set_column('A:A', 15)  # Seq Number
        worksheet.set_column('B:B', 30)  # Task Name
        worksheet.set_column('C:D', 15)  # Date, Deadline
        worksheet.set_column('E:E', 12)  # State

        # Title
        title = f"Task Report from {date_from or '...'} to {date_to or '...'}"
        worksheet.merge_range('A1:E1', title, title_format)
        worksheet.set_row(0, 25)

        row = 2
        headers = ['Seq Number', 'Task Name', 'Date', 'Deadline', 'State']

        for employee_name, employee_task_list in employee_tasks.items():
            worksheet.write(row, 0, employee_name, workbook.add_format({
                'bold': True, 'font_size': 12, 'bg_color': '#BDD7EE', 'align': 'left', 'valign': 'vcenter'
            }))
            row += 1

            for col_num, header in enumerate(headers):
                worksheet.write(row, col_num, header, header_format)
            row += 1

            for index, task in enumerate(employee_task_list):
                row_format = alt_row_format if index % 2 else string_format
                worksheet.write(row, 0, task.seq_number or '', row_format)
                worksheet.write(row, 1, task.name or '', row_format)
                worksheet.write(row, 2, task.date.strftime("%Y-%m-%d") if task.date else '', date_format)
                worksheet.write(row, 3, task.deadline.strftime("%Y-%m-%d") if task.deadline else '', date_format)
                worksheet.write(row, 4, task.state or '', row_format)
                row += 1

            row += 1  # Space between employees

        workbook.close()
        output.seek(0)

        file_name = f'Task_Report_{date_from or "unknown"}_to_{date_to or "unknown"}.xlsx'

        return request.make_response(
            output.getvalue(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', f'attachment; filename="{file_name}"'),
            ]
        )
