# -*- coding: utf-8 -*-

{
    'name': "INMATEC Module",
    'description': "INAMATEC Project Module",
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Addons',
    'license': 'AGPL-3',
    'version': '15.0.1.0',
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'mrp',
        'sale',
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
        'views/mrp/mrp_production_views.xml',

        # reports

        # Menus
    ],
    'demo': [],
    'installable': True,
    'application': False,
}
