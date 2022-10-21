# -*- coding: utf-8 -*-

{
    'name': "INMATEC Product Labels",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'AGPL-3',
    'version': '15.0.1.0',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'stock',
        # ---------------------
        # OCA
        # ---------------------
        # ---------------------
        # axxelia
        # ---------------------
    ],
    'data': [
        # data

        # Security

        # wizards

        # views

        # reports
        'report/stock/axx_product_label_report.xml',

        # Menus
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
