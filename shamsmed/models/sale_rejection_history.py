# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleRejectionHistory(models.Model):
    _name = 'sale.rejection.history'
    _description = 'Sale Rejection History'
    _order = 'date desc, time desc'

    sale_order_id = fields.Many2one(
        'sale.order',
        string='Quotation',
        required=True,
        ondelete='cascade'
    )
    previous_state_user_id = fields.Many2one(
        'res.users',
        string='Previous Responsible User',
        required=True
    )

    from_user_id = fields.Many2one(
        'res.users',
        string='From User',
        required=True
    )
    
    to_user_id = fields.Many2one(
        'res.users',
        string='To User',
        required=True
    )
    
    reason = fields.Text(
        string='Rejection Reason',
        required=True
    )

    date = fields.Date(
        string='Date',
        default=fields.Date.context_today,
        required=True
    )

    time = fields.Datetime(
        string='Time',
        default=fields.Datetime.now,
        required=True
    )

    state_from = fields.Char(
        string='From State',
        required=True
    )
    
    state_to = fields.Char(
        string='To State',
        required=True
    )
    
    # Computed fields for display
    from_user_name = fields.Char(
        string='From User Name',
        related='from_user_id.name',
        store=True
    )
    
    to_user_name = fields.Char(
        string='To User Name', 
        related='to_user_id.name',
        store=True
    )
    
    quotation_name = fields.Char(
        string='Quotation Number',
        related='sale_order_id.name',
        store=True
    )
