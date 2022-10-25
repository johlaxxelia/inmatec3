{
    'name': "Inmatec Revenue Report Module",
    'summary': """
        Inmatec Revenue Report
        """,
    'description': """
       Add the feature to have a custom revenue report.
    """,
    'author': "axxelia GmbH",
    'website': "http://www.axxelia.com",
    'category': 'Custom Add-On',
    'version': '15.0.1',
    # any module necessary for this one to work correctly
    'depends': [
        # ---------------------
        # Odoo
        # ---------------------
        'sale_crm',
        # ---------------------
        # Axxelia
        # ---------------------
    ],
    # always loaded
    'data': [
        # data

        # Security
        'security/ir.model.access.csv',

        # crm
        'views/crm/crm_lead_views.xml',

        # base

        # account

        # reports
        'views/reports/axx_revenue_report_views.xml',

        # wizards

        # Menus

        # Report Layout
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'assets': {
    },
    'installable': True,
    'application': True
}
