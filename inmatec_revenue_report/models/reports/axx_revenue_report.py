# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class AxxRevenueReport(models.Model):
    _name = "axx.revenue.report"
    _description = "Revenue Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    @api.model
    def _get_done_states(self):
        return ['sale', 'done', 'paid']

    name = fields.Char('Order Reference', readonly=True)
    date = fields.Datetime('Order Date', readonly=True)
    product_id = fields.Many2one('product.product', 'Product Variant', readonly=True)
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', readonly=True)
    product_uom_qty = fields.Float('Qty Ordered', readonly=True)
    qty_to_deliver = fields.Float('Qty To Deliver', readonly=True)
    qty_delivered = fields.Float('Qty Delivered', readonly=True)
    qty_to_invoice = fields.Float('Qty', readonly=True)
    qty_invoiced = fields.Float('Qty Invoiced', readonly=True)
    qty_to_revenue = fields.Float('Qty to Revenue', readonly=True)
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)
    user_id = fields.Many2one('res.users', 'Salesperson', readonly=True)
    price_total = fields.Float('Total', readonly=True)
    price_subtotal = fields.Float('Untaxed Total', readonly=True)
    untaxed_amount_to_invoice = fields.Float('Untaxed Amount To Invoice', readonly=True)
    untaxed_amount_invoiced = fields.Float('Untaxed Amount Invoiced', readonly=True)
    product_tmpl_id = fields.Many2one('product.template', 'Product', readonly=True)
    categ_id = fields.Many2one('product.category', 'Product Category', readonly=True)
    nbr = fields.Integer('# of Lines', readonly=True)
    pricelist_id = fields.Many2one('product.pricelist', 'Pricelist', readonly=True)
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', readonly=True)
    team_id = fields.Many2one('crm.team', 'Sales Team', readonly=True)
    country_id = fields.Many2one('res.country', 'Customer Country', readonly=True)
    industry_id = fields.Many2one('res.partner.industry', 'Customer Industry', readonly=True)
    commercial_partner_id = fields.Many2one('res.partner', 'Customer Entity', readonly=True)
    state = fields.Selection([
        ('draft', 'Draft Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Sales Done'),
        ('cancel', 'Cancelled'),
        ], string='Status', readonly=True)
    weight = fields.Float('Gross Weight', readonly=True)
    volume = fields.Float('Volume', readonly=True)

    discount = fields.Float('Discount %', readonly=True)
    discount_amount = fields.Float('Discount Amount', readonly=True)
    campaign_id = fields.Many2one('utm.campaign', 'Campaign')
    medium_id = fields.Many2one('utm.medium', 'Medium')
    source_id = fields.Many2one('utm.source', 'Source')
    expected_revenue = fields.Char('Expected Revenue', readonly=True)
    order_id = fields.Many2one('sale.order', 'Order #', readonly=True)

    def _select_sale(self, fields=None):
        if not fields:
            fields = {}
        select_ = """
            coalesce(min(sol.id), - so.id) AS id,
            sm.product_id AS product_id,
            pt.uom_id AS product_uom,
            count(*) AS nbr,
            so.name AS name,
            sp.scheduled_date AS date,
            so.state AS state,
            so.partner_id AS partner_id,
            so.user_id AS user_id,
            so.company_id AS company_id,
            so.campaign_id AS campaign_id,
            so.medium_id AS medium_id,
            so.source_id AS source_id,
            extract(epoch FROM avg(date_trunc('day', sp.scheduled_date) - date_trunc('day', so.create_date))) / (24 * 60 * 60)::decimal (16, 2) AS delay,
            pt.categ_id AS categ_id,
            so.pricelist_id AS pricelist_id,
            so.analytic_account_id AS analytic_account_id,
            so.team_id AS team_id,
            p.product_tmpl_id,
            partner.country_id AS country_id,
            partner.industry_id AS industry_id,
            partner.commercial_partner_id AS commercial_partner_id,
            sol.discount AS discount,
            so.id AS order_id,
            SUM(sm.product_uom_qty) AS product_uom_qty,
            SUM(sml.qty_done) AS qty_delivered,
            SUM(sm.product_uom_qty - sml.qty_done) AS qty_to_deliver,
            SUM(sol.qty_invoiced / u.factor * u2.factor) AS qty_invoiced,
            SUM(sol.qty_to_invoice / u.factor * u2.factor) AS qty_to_invoice,
            SUM(CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END) AS qty_to_revenue,
            SUM((sol.price_total * (CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END / (sol.product_uom_qty / u.factor * u2.factor))) / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END) AS price_total,
            SUM((sol.price_subtotal * (CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END / (sol.product_uom_qty / u.factor * u2.factor))) / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END) AS price_subtotal,
            SUM((sol.untaxed_amount_to_invoice * (CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END / (sol.product_uom_qty / u.factor * u2.factor))) / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END) AS untaxed_amount_to_invoice,
            SUM((sol.untaxed_amount_invoiced * (CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END / (sol.product_uom_qty / u.factor * u2.factor))) / CASE COALESCE(so.currency_rate, 0) WHEN 0 THEN 1.0 ELSE so.currency_rate END) AS untaxed_amount_invoiced,
            SUM(p.weight * CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END) AS weight,
            SUM(p.volume * CASE WHEN sp.date_done IS NULL THEN sm.product_uom_qty ELSE sml.qty_done END) AS volume,
            (SELECT
                'Expected Qty: ' || SUM(quantity) || ', Expected Revenue: ' || SUM(expected_revenue)
            FROM
                axx_crm_expected_revenue
            WHERE
                product_id = sm.product_id
                AND sp.scheduled_date BETWEEN date_start
                AND date_end
                AND(partner_id = so.partner_id
                    OR partner_id IS NULL)) AS expected_revenue
        """

        for field in fields.values():
            select_ += field
        return select_

    def _from_sale(self, from_clause=''):
        from_ = """
                sale_order_line sol
                JOIN stock_move sm ON sm.sale_line_id = sol.id
                LEFT JOIN stock_move_line sml ON sml.move_id = sm.id
                JOIN stock_picking sp ON sm.picking_id = sp.id
                JOIN stock_picking_type spt ON sp.picking_type_id = spt.id
                JOIN product_product p ON sm.product_id = p.id
                JOIN product_template pt ON p.product_tmpl_id = pt.id
                JOIN sale_order so ON sol.order_id = so.id
                JOIN res_partner partner ON so.partner_id = partner.id
                JOIN uom_uom u ON (u.id = sol.product_uom)
                JOIN uom_uom u2 ON (u2.id = pt.uom_id)
                %s
        """ % from_clause
        return from_

    def _group_by_sale(self, groupby=''):
        groupby_ = """
            sm.product_id,
            sol.order_id,
            pt.uom_id,
            pt.categ_id,
            so.name,
            sp.scheduled_date,
            so.partner_id,
            so.user_id,
            so.state,
            so.company_id,
            so.campaign_id,
            so.medium_id,
            so.source_id,
            so.pricelist_id,
            so.analytic_account_id,
            so.team_id,
            p.product_tmpl_id,
            partner.country_id,
            partner.industry_id,
            partner.commercial_partner_id,
            sol.discount,
	        expected_revenue,
            so.id %s
        """ % (groupby)
        return groupby_

    def _query(self, with_clause='', fields=None, groupby='', from_clause=''):
        if not fields:
            fields = {}
        with_ = ("WITH %s" % with_clause) if with_clause else ""
        return "%s (SELECT %s FROM %s WHERE spt.code = 'outgoing' GROUP BY %s)" % \
               (with_, self._select_sale(fields), self._from_sale(from_clause), self._group_by_sale(groupby))

    def init(self):
        # self._table = sale_report
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, self._query()))
