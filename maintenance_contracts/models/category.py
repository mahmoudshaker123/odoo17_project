from odoo import models, fields, api
from datetime import datetime, timedelta, date
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class CategoryHistory(models.Model):
    _name = 'category'
    _description = 'Category History'

    name = fields.Char(string='Name')