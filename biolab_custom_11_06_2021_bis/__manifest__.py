# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BIOLAB Personnalisation',
    'description': """

    """,
    'category': 'Custom',
    'sequence': 32,
    'depends': ['base', 'sale_management', 'purchase', 'account', 'stock'],
    'data': [
        "views/report_css.xml",
        "reports/report_template_view.xml",
        "reports/report_sale_order_template.xml",
        "reports/report_stock_picking_template.xml",
        "reports/report_account_move_template.xml",
        "reports/report_menu.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
        "views/res_partner_view.xml",
        "views/product_view.xml",
        "views/stock_view.xml",
    ],
    'qweb': [
    ],
    'license': 'OEEL-1',
    'auto_install': True,
}
