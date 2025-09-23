from odoo import api, fields, models


class ResPartnerCustomerMetrics(models.Model):
    _name = "res.partner.customer_metrics"
    _description = "Customer Sales Metrics"
    _order = "total_sales desc, order_count desc"

    customer_id = fields.Many2one(
        "res.partner",
        string="Customer",
        required=True,
        index=True,
        ondelete="cascade",
    )

    total_sales = fields.Monetary(
        string="Total Sales",
        currency_field="currency_id",
        compute="_compute_metrics",
        store=True,   # ✅ now values are stored in DB
    )

    order_count = fields.Integer(
        string="Order Count",
        compute="_compute_metrics",
        store=True,   # ✅ stored as well
    )

    currency_id = fields.Many2one(
        "res.currency",
        string="Currency",
        related="customer_id.company_id.currency_id",
        store=True,
        readonly=True,
    )

    _sql_constraints = [
        ("unique_customer", "unique(customer_id)", "Metrics already exists for this customer."),
    ]

    def name_get(self):
        return [(rec.id, rec.customer_id.display_name) for rec in self]

    @api.depends("customer_id")
    def _compute_metrics(self):
        """Compute total sales and order count from sale.order for each customer."""
        partner_ids = self.mapped("customer_id").ids
        totals, counts = {}, {}

        if partner_ids:
            # include all orders for this customer or its contacts
            domain = [("partner_id", "child_of", partner_ids), ("state", "in", ["sale", "done"])]
            groups = self.env["sale.order"].sudo().read_group(
                domain=domain,
                fields=["amount_total:sum", "id:count"],
                groupby=["partner_id"],
            )
            for g in groups:
                if g.get("partner_id"):
                    partner_id = g["partner_id"][0]
                    totals[partner_id] = g.get("amount_total_sum", 0.0) or 0.0
                    counts[partner_id] = g.get("id_count", 0) or 0

        for rec in self:
            rec.total_sales = totals.get(rec.customer_id.id, 0.0)
            rec.order_count = counts.get(rec.customer_id.id, 0)

    @api.model
    def get_top_customers(self, limit=5):
        """Return top N customers by total sales as list of dicts."""
        records = self.search([], order="total_sales desc, order_count desc", limit=limit)
        currency = self.env.company.currency_id
        return [
            {
                "name": rec.customer_id.display_name,
                "total_sales": rec.total_sales or 0.0,
                "order_count": rec.order_count or 0,
                "currency": currency.name,
            }
            for rec in records
        ]

    @api.model
    def create_metrics_for_customers(self):
        """Create metrics records for customers with confirmed orders using commercial partner IDs."""
        domain = [("state", "in", ["sale", "done"])]
        groups = self.env["sale.order"].read_group(
            domain=domain,
            fields=["partner_id"],
            groupby=["partner_id"],
        )
        partner_ids = [g["partner_id"][0] for g in groups if g.get("partner_id")]
        partners = self.env["res.partner"].browse(partner_ids)
        commercial_ids = partners.mapped("commercial_partner_id").ids

        existing = self.search([("customer_id", "in", commercial_ids)])
        existing_partners = set(existing.mapped("customer_id").ids)

        to_create = [{"customer_id": pid} for pid in commercial_ids if pid not in existing_partners]
        if to_create:
            self.create(to_create)
