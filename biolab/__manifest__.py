# -*- coding: utf-8 -*-
{
    'name': "biolab",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        biolab module for custom reports.
    """,

    'author': "biolab",
    'website': "https://biolabsarl.ci/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    # always loaded
    'data': [
        #'security/ir.model.access.csv',
        'report/report.xml',
        'report/account_report.xml',
        'report/sale_report.xml',
        'report/report_invoice.xml',
        'report/report_deliveryslip.xml',
        'report/report_invoice_without_header.xml',
        'report/purchase_order_templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
