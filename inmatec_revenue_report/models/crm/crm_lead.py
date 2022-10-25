from odoo import api, fields, models, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    axx_product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True
    )
    axx_qty = fields.Float(
        string="Quantity"
    )
    axx_expected_revenue_ids = fields.One2many(
        'axx.crm.expected.revenue',
        'crm_lead_id',
        string='Expected Revenues Plan',
        readonly=True
    )

    _sql_constraints = [
        (
            'check_axx_qty',
            'CHECK(axx_qty > 0)',
            'Quantity must be greater than zero!'
        )
    ]

    def _create_revenue_plan(self):
        crm_expected_revenue_env = self.env['axx.crm.expected.revenue']
        for lead in self:
            if lead.date_deadline and any([lead.expected_revenue, lead.recurring_revenue]):
                num_of_months = lead.recurring_plan and lead.recurring_plan.number_of_months or 0
                crm_expected_revenue_env.create_plan(
                    lead.id, num_of_months, lead.date_deadline,
                    lead.expected_revenue + lead.recurring_revenue * num_of_months,
                    lead.axx_product_id.id, lead.axx_qty
                )
        return True

    @api.model
    def create(self, vals):
        rec = super(CrmLead, self).create(vals)
        rec._create_revenue_plan()
        return rec

    def write(self, vals):
        res = super(CrmLead, self).write(vals)
        if any([
            'date_deadline' in vals,
            'expected_revenue' in vals,
            'recurring_revenue' in vals,
            'recurring_plan' in vals,
            'axx_product_id' in vals,
            'axx_qty' in vals,
        ]):
            self.mapped("axx_expected_revenue_ids").unlink()
            self._create_revenue_plan()
        return res

    def unlink(self):
        self.mapped("axx_expected_revenue_ids").unlink()
        return super(CrmLead, self).unlink()
