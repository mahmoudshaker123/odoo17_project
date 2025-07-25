from odoo import models , fields , api
from odoo.exceptions import ValidationError


class TaskManagement(models.Model):
    _name = 'task.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char(copy=False)
    seq_number = fields.Char(default='New', readonly=True ,string='Number' , copy=False)
    employee = fields.Many2one('hr.employee')
    assignees = fields.Many2many('res.users' , default=lambda self: [self.env.uid])
    date = fields.Datetime(default=fields.Datetime.now , required=1)
    deadline = fields.Datetime(required=1)
    state = fields.Selection([
        ('draft','Draft'),
        ('in_progress','In Progress'),
        ('done','Done'),
    ],
        default='draft'
    )
    description = fields.Text()
    extra_info = fields.Text(string='Extra Info')

    _sql_constraints = [
        ('unique_name', 'UNIQUE(name)', 'This name already exists.')
    ]


    def action_draft(self):
        for rec in self:
            rec.state= 'draft'

    def action_in_progress(self):
        for rec in self:
            rec.state= 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state= 'done'

    def action_change_in_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_progress'

    def action_change_done(self):
        for rec in self:
            if rec.state == 'in_progress':
                rec.state = 'done'


    @api.model
    def create(self, vals):
        res = super(TaskManagement ,self).create(vals)
        if res.seq_number =='New':
            res.seq_number = self.env['ir.sequence'].next_by_code('task_management_seq')
        return res

    @api.constrains('state', 'employee')
    def _check_max_in_progress_tasks(self):
        for record in self:
            if record.state == 'in_progress' and record.employee:
                count = self.search_count([
                    ('employee', '=', record.employee.id),
                    ('state', '=', 'in_progress'),
                    ('id', '!=', record.id)
                ])
                if count >= 5:
                    raise ValidationError("No more than 5 tasks .")

    def unlink(self):
        for rec in self:
            if rec.state != 'draft':
                raise ValidationError("You can only delete tasks in Draft state.")
            if self.env.user not in rec.assignees:
                raise ValidationError("Only assignees can delete this task.")
        return super().unlink()












