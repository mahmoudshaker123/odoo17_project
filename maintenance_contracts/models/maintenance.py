from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
import logging

_logger = logging.getLogger(__name__)



class MaintenanceContract(models.Model):
    _name = 'maintenance.contract'
    _description = 'Maintenance Contract'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # -------------------------
    # Fields
    # -------------------------
    state = fields.Selection([
        ('draft', 'Draft'),
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('nearly_expired', 'Nearly Expired'),
        ('expired', 'Expired'),
    ], default='draft', string="Status", compute="_compute_status", store=True, tracking=True)

    billing_type = fields.Selection([
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly')
    ], string='Billing Type', required=True, default='monthly')

    payment_timing = fields.Selection([
        ('prepaid', 'Prepaid'),
        ('postpaid', 'Postpaid')
    ], string='Payment Timing', required=True, default='prepaid')

    customer_name = fields.Many2one('res.partner', string='Customer Name', required=True)
    category = fields.Many2one('category', string='Category', required=True)
    contract_description = fields.Char(string='Contract Description')
    contract_date = fields.Date(string='Contract Date', required=True)
    total_cost = fields.Float(string='Price without VAT', required=True, help="The current total cost of the contract")
    vat = fields.Float(string='Increase Percentage', required=True, default=0.0,
                       help="VAT percentage to be added annually")
    vatt = fields.Float(string="VAT", default=0.0, help="Enter the additional value to be added to Total Cost")
    next_addition_date = fields.Date(string='Renewal Contract Date', required=True)
    employee_name = fields.Many2one('hr.employee', string='Employee Name', required=True)
    reminder_email = fields.Char(string="Reminder Email")

    attachment_ids = fields.One2many(
        'maintenance.contract.attachment',
        'maintenance_contract_id',
        string="Attachments"
    )
    price_with_vat = fields.Float(string='Price with VAT', compute='_compute_price_with_vat', store=True, readonly=True)
    total_price_with_inc = fields.Float(string='Total Price with Inc. & without VAT',
                                        compute='_compute_total_price_with_inc', store=True, readonly=True)
    total_cost_after = fields.Float(string='Total Cost With Vat & Inc.', compute='_compute_total_cost_after',
                                    store=True, readonly=True)
    next_vat_update = fields.Date(string='Next VAT Update', compute='_compute_next_vat_update', store=True)

    message_ids = fields.One2many('mail.message', 'res_id', domain=[('model', '=', 'maintenance.contract')],
                                  string="Messages", help="Messages or log history related to the contract")
    message_follower_ids = fields.Many2many('res.partner', 'maintenance_contract_res_partner_rel', 'contract_id',
                                            'partner_id', string="Followers")

    # -------------------------
    # Compute Methods
    # -------------------------
    @api.depends('total_cost', 'vat')
    def _compute_total_price_with_inc(self):
        for record in self:
            record.total_price_with_inc = record.total_cost * (1 + record.vat)

    @api.depends('total_cost', 'vatt')
    def _compute_price_with_vat(self):
        for record in self:
            record.price_with_vat = record.total_cost * (1 + record.vatt)

    @api.depends('total_cost', 'vat', 'vatt')
    def _compute_total_cost_after(self):
        for record in self:
            vat_amount = record.total_cost * record.vat if record.vat else 0
            vatt_amount = record.total_cost * record.vatt if record.vatt else 0
            record.total_cost_after = record.total_cost + vat_amount + vatt_amount

    @api.depends('contract_date', 'next_addition_date')
    def _compute_status(self):
        today = fields.Date.today()
        for record in self:
            if record.next_addition_date:
                nearly_expired_date = record.next_addition_date - timedelta(days=30)
                if record.next_addition_date < today:
                    record.state = 'expired'
                elif nearly_expired_date <= today <= record.next_addition_date:
                    record.state = 'nearly_expired'
                elif record.contract_date and record.contract_date > today:
                    record.state = 'upcoming'
                elif record.contract_date and record.contract_date <= today:
                    record.state = 'active'
            else:
                record.state = 'draft'

    # -------------------------
    # Create & Write
    # -------------------------
    @api.model
    def create(self, vals):
        today = fields.Date.today()

        if 'total_cost' not in vals or vals['total_cost'] is None:
            vals['total_cost'] = 0.0

        if 'contract_date' not in vals or vals['contract_date'] is None:
            vals['contract_date'] = today

        if 'contract_date' in vals and vals['contract_date']:
            contract_date = fields.Date.from_string(vals['contract_date'])
            vals['state'] = 'upcoming' if contract_date > today else 'active'

        if 'next_addition_date' in vals and vals['next_addition_date']:
            next_addition_date = fields.Date.from_string(vals['next_addition_date'])
            if next_addition_date < today:
                vals['state'] = 'expired'

        return super(MaintenanceContract, self).create(vals)

    def write(self, vals):
        if 'total_cost' not in vals or vals['total_cost'] is None:
            vals['total_cost'] = self.total_cost

        if 'contract_description' not in vals or vals['contract_description'] is None:
            vals['contract_description'] = self.contract_description

        if 'contract_date' not in vals or vals['contract_date'] is None:
            vals['contract_date'] = self.contract_date

        if 'next_addition_date' not in vals or vals['next_addition_date'] is None:
            vals['next_addition_date'] = self.next_addition_date

        return super(MaintenanceContract, self).write(vals)

    # -------------------------
    # Constraints
    # -------------------------
    @api.constrains('next_addition_date', 'contract_date')
    def _check_renewal_date(self):
        for record in self:
            if record.next_addition_date and record.contract_date:
                if record.next_addition_date < record.contract_date:
                    raise ValidationError("The Renewal Contract Date cannot be earlier than the Contract Date.")


    # -------------------------
    # Return contracts with 30 days
    # -------------------------
    def _contracts_needing_reminder(self):
        """Return contracts with 30 days or less remaining to next_addition_date"""
        today = fields.Date.today()
        threshold_date = today + timedelta(days=30)
        return self.search([
            ('next_addition_date', '<=', threshold_date),
            ('next_addition_date', '>=', today),
        ])



    # -------------------------
    # cron
    # -------------------------

    def send_remind_email(self):
        """Send reminder email to contracts nearly expired"""
        nearly_expired_contracts = self.search([('state', '=', 'nearly_expired')])
        for contract in nearly_expired_contracts:
            if contract.reminder_email:
                mail_values = {
                    'subject': f"🔔 Reminder: Contract {contract.customer_name.name or ''} is nearly expired",
                    'body_html': f"""
                        <div style="font-family:Arial, sans-serif; color:#333; line-height:1.6;">
                            <h3 style="color:#d35400;">🔔 تنبيه بخصوص العقد</h3>
                            <p>مرحبًا,</p>
                            <table style="border-collapse:collapse; margin:10px 0;">
                                <tr>
                                    <td style="padding:5px 10px;"><b>العميل:</b></td>
                                    <td style="padding:5px 10px;">{contract.customer_name.name or ''}</td>
                                </tr>
                                <tr>
                                    <td style="padding:5px 10px;"><b>العقد:</b></td>
                                    <td style="padding:5px 10px;">{contract.contract_description or ''}</td>
                                </tr>
                                <tr>
                                    <td style="padding:5px 10px;"><b>تاريخ انتهاء العقد:</b></td>
                                    <td style="padding:5px 10px;">{contract.next_addition_date}</td>
                                </tr>
                            </table>
                            <p>
                                هذا تذكير بأن العقد الخاص بهذه الشركة أو العميل على وشك الانتهاء.  
                                يُرجى اتخاذ اللازم لتجديد العقد في الوقت المناسب.
                            </p>

                            <hr style="margin:20px 0;"/>

                            <h3 style="color:#2980b9;">🔔 Contract Reminder</h3>
                            <p>Hello,</p>
                            <table style="border-collapse:collapse; margin:10px 0;">
                                <tr>
                                    <td style="padding:5px 10px;"><b>Customer:</b></td>
                                    <td style="padding:5px 10px;">{contract.customer_name.name or ''}</td>
                                </tr>
                                <tr>
                                    <td style="padding:5px 10px;"><b>Contract:</b></td>
                                    <td style="padding:5px 10px;">{contract.contract_description or ''}</td>
                                </tr>
                                <tr>
                                    <td style="padding:5px 10px;"><b>Expiration Date:</b></td>
                                    <td style="padding:5px 10px;">{contract.next_addition_date}</td>
                                </tr>
                            </table>
                            <p>
                                This is a reminder that the contract is about to expire.  
                                Please take the necessary action to renew it on time.
                            </p>

                            <p style="margin-top:20px;">Thanks,<br/><b>Contracts Management System</b></p>
                        </div>
                    """,
                    'email_to': contract.reminder_email,
                }
                self.env['mail.mail'].create(mail_values).send()


    def _get_billing_period_months(self):
        """Return number of months for the billing period based on billing_type."""
        self.ensure_one()
        if self.billing_type == 'monthly':
            return 1
        if self.billing_type == 'quarterly':
            return 3
        return 12

    def _get_next_period_start(self, reference_date=None):
        """Compute the next period start date on or after reference_date, aligned to contract_date."""
        self.ensure_one()
        today = fields.Date.today()
        ref_date = reference_date or today
        base = self.contract_date or ref_date
        period_months = self._get_billing_period_months()

        # Align by adding months until we reach or pass ref_date
        current = base
        # Guard against infinite loops if inputs are odd
        for _ in range(0, 500):
            if current >= ref_date:
                return current
            current = current + relativedelta(months=+period_months)
        return ref_date

    def _get_period_bounds(self, reference_date=None):
        """Return (period_start, period_end) for the period that ends next (postpaid) or starts next (prepaid).

        - For prepaid: due date is next period start; bounds represent that upcoming period
        - For postpaid: due date is the end of the current period that will end soon
        """
        self.ensure_one()
        next_start = self._get_next_period_start(reference_date)
        period_months = self._get_billing_period_months()
        prev_start = next_start + relativedelta(months=-period_months)
        prev_end = next_start + timedelta(days=-1)

        if self.payment_timing == 'prepaid':
            # Upcoming period [next_start, next_start + period - 1 day]
            upcoming_end = next_start + relativedelta(months=+period_months) + timedelta(days=-1)
            return next_start, upcoming_end
        # Postpaid: current period [prev_start, prev_end]
        return prev_start, prev_end

    def _get_period_amount(self):
        """Compute the amount due for one billing period (without taxes adjustments beyond what's stored)."""
        self.ensure_one()
        period_months = self._get_billing_period_months()
        if period_months == 12:
            return self.total_cost
        # Pro-rate based on months over a year
        return (self.total_cost / 12.0) * period_months

    def send_billing_invoice_reminder(self):
        """Send billing invoice reminders based on billing_type and payment_timing.

        Logic:
        - Determine due date:
          - prepaid: due date = next period start
          - postpaid: due date = end of the current period
        - Notify when due date is within next 7 days
        """
        today = fields.Date.today()
        threshold_date = today + timedelta(days=3)

        contracts = self.search([('state', 'in', ['active', 'nearly_expired'])])
        for contract in contracts:
            if not contract.reminder_email:
                continue

            period_start, period_end = contract._get_period_bounds(reference_date=today)
            # Determine due date by payment timing
            due_date = period_start if contract.payment_timing == 'prepaid' else period_end

            if not (today <= due_date <= threshold_date):
                continue

            amount = contract._get_period_amount()
            billing_label = dict(contract._fields['billing_type'].selection).get(contract.billing_type, contract.billing_type)
            timing_label = dict(contract._fields['payment_timing'].selection).get(contract.payment_timing, contract.payment_timing)

            subject = f"🧾 Invoice Reminder: {billing_label} ({timing_label}) for {contract.customer_name.name or ''}"
            body_html = f"""
                <div style="font-family:Arial, sans-serif; color:#333; line-height:1.6;">
                    <h3 style="color:#27ae60;">🧾 تذكير فاتورة الصيانة</h3> 
                    <p>مرحبًا,</p>
                    <table style="border-collapse:collapse; margin:10px 0;">
                        <tr>
                            <td style="padding:5px 10px;"><b>العميل:</b></td>
                            <td style="padding:5px 10px;">{contract.customer_name.name or ''}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>نوع الفوترة:</b></td>
                            <td style="padding:5px 10px;">{billing_label}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>توقيت السداد:</b></td>
                            <td style="padding:5px 10px;">{timing_label}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>فترة الفاتورة:</b></td>
                            <td style="padding:5px 10px;">{period_start} → {period_end}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>تاريخ الاستحقاق:</b></td>
                            <td style="padding:5px 10px;">{due_date}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>المبلغ المستحق:</b></td>
                            <td style="padding:5px 10px;">{amount:.2f}</td>
                        </tr>
                    </table>
                    <p>هذا تذكير بإصدار/سداد الفاتورة طبقًا للنوع ({billing_label}) والتوقيت ({timing_label}).</p>

                    <hr style="margin:20px 0;"/>

                    <h3 style="color:#2980b9;">🧾 Maintenance Invoice Reminder</h3>
                    <p>Hello,</p>
                    <table style="border-collapse:collapse; margin:10px 0;">
                        <tr>
                            <td style="padding:5px 10px;"><b>Customer:</b></td>
                            <td style="padding:5px 10px;">{contract.customer_name.name or ''}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>Billing Type:</b></td>
                            <td style="padding:5px 10px;">{billing_label}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>Payment Timing:</b></td>
                            <td style="padding:5px 10px;">{timing_label}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>Invoice Period:</b></td>
                            <td style="padding:5px 10px;">{period_start} → {period_end}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>Due Date:</b></td>
                            <td style="padding:5px 10px;">{due_date}</td>
                        </tr>
                        <tr>
                            <td style="padding:5px 10px;"><b>Amount Due:</b></td>
                            <td style="padding:5px 10px;">{amount:.2f}</td>
                        </tr>
                    </table>
                    <p>Please issue/pay the invoice according to the schedule.</p>

                    <p style="margin-top:20px;">Thanks,<br/><b>Contracts Management System</b></p>
                </div>
            """

            self.env['mail.mail'].create({
                'subject': subject,
                'body_html': body_html,
                'email_to': contract.reminder_email,
            }).send()


# -------------------------
# Attachment Model
# -------------------------

class MaintenanceContractAttachment(models.Model):
    _name = 'maintenance.contract.attachment'
    _description = 'Maintenance Contract Attachment'

    name = fields.Char(string='File Name')
    file_data = fields.Binary(string='Attachment File', attachment=True)
    file_name = fields.Char(string='Filename')
    maintenance_contract_id = fields.Many2one('maintenance.contract', string='Maintenance Contract')
