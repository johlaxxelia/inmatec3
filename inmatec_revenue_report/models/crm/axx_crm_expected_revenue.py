from pkg_resources import require
from odoo import models, fields, api, _

from dateutil.relativedelta import relativedelta
from datetime import timedelta


class AxxCrmExpectedRevenue(models.Model):
    _name = 'axx.crm.expected.revenue'

    crm_lead_id = fields.Many2one(
        comodel_name="crm.lead",
        string="CRM Lead",
        required=True
    )
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        related="crm_lead_id.partner_id",
        store=True,
        readonly=True
    )
    date_start = fields.Date(
        string="Start Date",
        required=True
    )
    date_end = fields.Date(
        string="End Date",
        required=True
    )
    product_id = fields.Many2one(
        comodel_name="product.product",
        string="Product",
        required=True
    )
    quantity = fields.Float(
        string="Quantity"
    )
    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Currency",
        related="crm_lead_id.company_currency"
    )
    expected_revenue = fields.Monetary(
        string="Exptected Revenue",
        currency_field='currency_id',
    )

    def create_plan(self, lead_id, num_of_months, date_end, amount, product_id, qty):
        if not amount or not date_end or not lead_id:
            return False
        if not num_of_months:
            self.create({
                'crm_lead_id': lead_id,
                'date_start': date_end,
                'date_end': date_end,
                'product_id': product_id,
                'quantity': qty,
                'expected_revenue': amount
            })
            return True
        start_date = date_end - relativedelta(months=num_of_months) + timedelta(days=1)
        end_date = start_date + relativedelta(months=1) - timedelta(days=1)
        for i in range(num_of_months):
            self.create({
                'crm_lead_id': lead_id,
                'date_start': start_date,
                'date_end': end_date,
                'product_id': product_id,
                'quantity': qty / num_of_months,
                'expected_revenue': amount / num_of_months
            })
            start_date = end_date + timedelta(days=1)
            end_date = end_date + relativedelta(months=1)
        return True
