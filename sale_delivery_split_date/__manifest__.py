# -*- coding: utf-8 -*-

{
    "name": "Sale Delivery Split Date",
    "version": "15.0.1.0",
    "summary": "Sale Deliveries split by date",
    "category": "Sales Management",
    "license": "AGPL-3",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    "depends": [
        "sale_order_line_date",
        "sale_procurement_group_by_line",
    ],
    "data": [
        "views/stock_picking.xml",
    ],
    "installable": True,
}
