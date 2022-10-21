# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ProductLabelLayout(models.TransientModel):
    _inherit = "product.label.layout"

    print_format = fields.Selection(selection_add=[
        ('axx_product_label', 'Product Label'),
    ], default="axx_product_label", ondelete={'axx_product_label': 'set default'})

    def _prepare_report_data(self):
        xml_id, data = super(ProductLabelLayout, self)._prepare_report_data()
        if self.print_format == 'axx_product_label':
            xml_id = 'inmatec_product_label.report_axx_product_label'
            data['product_move_ids'] = self.move_line_ids.ids
            if self.picking_quantity == 'picking':
                data['quantity_by_product'] = {line.id: (line.qty_done / line.move_id.product_packaging_id.qty) if line.move_id.product_packaging_id else 1 for line in self.move_line_ids}
            else:
                data['quantity_by_product'] = {line.id: self.custom_quantity for line in self.move_line_ids}
        return xml_id, data


