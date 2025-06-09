from odoo import models , fields

class TaskManagement(models.Model):
    _name = 'task.management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name=fields.Char()
    seq_number = fields.Char(default='New', readonly=True ,string='Number')
    employee = fields.Many2one('hr.employee')
    assignees = fields.Many2many('res.users' , default=lambda self: [self.env.uid])
    date = fields.Datetime()
    deadline = fields.Datetime()
    state = fields.Selection([
        ('draft','Draft'),
        ('in_progress','In Progress'),
        ('done','Done'),
    ],
        default='draft'
    )
    description = fields.Text()
    extra_info = fields.Text(string='Extra Info')


    def action_draft(self):
        for rec in self:
            rec.state= 'draft'

    def action_in_progress(self):
        for rec in self:
            rec.state= 'in_progress'

    def action_done(self):
        for rec in self:
            rec.state= 'done'
