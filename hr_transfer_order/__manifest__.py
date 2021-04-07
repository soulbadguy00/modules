# -*- coding: utf-8 -*-
{
    'name': "Hr Ordre de virement",

    'summary': """
    """,

    'description': """
        Gestion des ordres de virement.
    """,

    'author': "Rodolphe Agnero",
    'website': "www.Rodolphe Agnero.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '2.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'hr_cnce'],

    # always loaded
    'data': [
        "security/ir.model.access.csv",
        "reports/templates/layout_view.xml",
        "reports/report_transfer_order.xml",
        "reports/report_menu.xml",
        "wizards/hrTransferOrderView.xml",
        "views/asset_backend.xml",
    ],
    # only loaded in demonstration mode
    'demo': [],
}
