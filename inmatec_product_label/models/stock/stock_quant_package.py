# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockQuantPackage(models.Model):
    _inherit = "stock.quant.package"

    axx_move_line_ids = fields.One2many('stock.move.line', 'result_package_id')

