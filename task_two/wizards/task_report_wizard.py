from odoo import models, fields


class TaskReportWizard(models.TransientModel):
    _name = 'task.report.wizard'
    _description = 'Task Excel Report Wizard'

    date_from = fields.Date(string="Date From")
    date_to = fields.Date(string="Date To")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    ], string="State")
    employee_id = fields.Many2one('hr.employee', string="Employee")

    def generate_excel_report(self):
        base_url = '/task/excel/report'
        params = []

        if self.date_from:
            params.append(f'date_from={self.date_from}')
        if self.date_to:
            params.append(f'date_to={self.date_to}')
        if self.state:
            params.append(f'state={self.state}')
        if self.employee_id:
            params.append(f'employee_id={self.employee_id.id}')

        query_string = '&'.join(params)
        full_url = f'{base_url}?{query_string}'

        return {
            'type': 'ir.actions.act_url',
            'url': full_url,
            'target': 'new',
        }
