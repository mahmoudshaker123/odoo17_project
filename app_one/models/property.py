from email.policy import default

from odoo import models , fields , api
from odoo.exceptions import ValidationError


class Property(models.Model):
    _name = 'property'
    _inherit =['mail.thread','mail.activity.mixin']
    _description = 'Real Estate Property'

    name = fields.Char(required=1)
    description = fields.Text(tracking=1)
    postcode = fields.Char(required=1)
    date_availability = fields.Date(tracking=1)
    expected_selling_date = fields.Date(tracking=1)
    is_late = fields.Boolean()
    expected_price = fields.Float()
    selling_price = fields.Float()
    diff = fields.Float(compute='_compute_diff')
    bedrooms = fields.Integer()
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    active = fields.Boolean(default=True)

    garden_orientation = fields.Selection(
        [
            ('north', 'North'),
            ('south', 'South'),
            ('east', 'East'),
            ('west', 'West')
        ],
        default='south'
    )

    owner_id = fields.Many2one('owner')
    tag_ids = fields.Many2many('tag')
    owner_address = fields.Char(related='owner_id.address')
    owner_phone = fields.Char(related='owner_id.phone')

    line_ids=fields.One2many('property.line','property_id')


    state = fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('sold','Sold'),
        ('closed','Closed'),
    ],
        default='draft'
    )

    _sql_constraints = [
        ('unique_name','unique("name")','This name is exist')
    ]

    @api.depends('expected_price','selling_price')
    def _compute_diff(self):
        for rec in self:
            rec.diff = rec.expected_price - rec.selling_price


    @api.onchange('expected_price')
    def _onchange_expected_price(self):
        for rec in self:
            print("inside _onchange_expected_price method")
            return{
                'warning': {'title':'warning' , 'message':'negative_value. ' , 'type':'notification'}
            }

    @api.constrains('bedrooms')
    def _check_bedrooms_greater_zero(self):
        for rec in self:
            if rec.bedrooms == 0:
                raise ValidationError('please add valid number of bedrooms')



    def action_draft(self):
        for rec in self:
            print("inside draft actions")
            rec.state= 'draft'

    def action_pending(self):
        for rec in self:
            print("inside pending actions")
            rec.state= 'pending'

    def action_sold(self):
        for rec in self:
            print("inside sold actions")
            rec.state= 'sold'

    def action_closed(self):
        for rec in self:
            rec.state= 'closed'


    def check_expected_selling_date(self):
        property_ids = self.search([])
        for rec in property_ids:
            if rec.expected_selling_date and rec.expected_selling_date < fields.date.today():
                rec.is_late = True



    # @api.model_create_multi
    # def create(self, vals):
    #     res = super(Property, self).create(vals)
    #     return res
    #
    # def write(self, vals):
    #     res = super(Property, self).write(vals)
    #     return res
    #
    # def _search(self, domain, offset=0, limit=None, order=None, access_rights_uid=None):
    #     res = super(Property, self)._search(domain, offset=0, limit=None, order=None, access_rights_uid=None)
    #     return res
    #
    # def unlink(self):
    #     res = super(Property, self).unlink()
    #     return res



class PropertyLine(models.Model):
    _name = 'property.line'

    property_id= fields.Many2one('property')
    area = fields.Float()
    description = fields.Char()