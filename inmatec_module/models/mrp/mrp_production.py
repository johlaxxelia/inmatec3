# -*- coding: utf-8 -*-

from odoo import api, fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"

    axx_partner_id = fields.Many2one('res.partner', compute="_compute_partner_id", string="Customer")

    @api.depends()
    def _compute_partner_id(self):
        for mo in self:
            sale_order = mo.procurement_group_id.mrp_production_ids.move_dest_ids.group_id.sale_id[:1]
            mo.axx_partner_id = sale_order.partner_id.id
