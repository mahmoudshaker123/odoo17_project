from odoo import fields , models ,api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    employee_number=fields.Integer(string='Employee Number')
    has_related_tasks = fields.Boolean(string="Has Related Tasks", compute="_compute_has_related_tasks" ,store=True)
    task_count = fields.Integer(string="Tasks Count", compute="_compute_task_count", store=False)

    def _compute_has_related_tasks(self):
        for rec in self:
            count = self.env['task.management'].search_count([
                ('employee', '=', rec.id),
                ('state', '=', 'in_progress')
            ])
            rec.has_related_tasks = count > 0

    def _compute_task_count(self):
        for rec in self:
            rec.task_count = self.env['task.management'].search_count([
                ('employee', '=', rec.id),
                ('state', '=', 'in_progress')
            ])


    _sql_constraints = [
        ('unique_employee_number', 'unique("employee_number")', 'This employee number is exist')
    ]

    def action_open_related_task(self):
        action = self.env['ir.actions.actions']._for_xml_id('task_two.task_management_action')
        tree_view_id = self.env.ref('task_two.task_management_tree_view').id
        form_view_id = self.env.ref('task_two.task_management_form_view').id

        action.update({
            'domain': [
                ('employee', '=', self.id),
                ('state', '=', 'in_progress')
            ],
            'context': {
                'default_employee': self.id
            },
            'views': [
                (tree_view_id, 'tree'),
                (form_view_id, 'form')
            ],
            'view_mode': 'tree,form',
        })
        return action






