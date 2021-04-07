##############################################################################
#
# Copyright (c) 2020 - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_cmu
# ##############################################################################
{
    "name": "Rapports CMU",
    "version": "1.0",
    "author": "Rodolphe Agnero",
    'category': 'Localization',
    "website": "www.Rodolphe Agnero.net",
    "depends": ["base", "hr","report_xlsx"],
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/ir.model.access.csv",
        "views/hrCMUWizardView.xml",
        "reports/menu_report.xml",
    ],
    "installable": True
}
