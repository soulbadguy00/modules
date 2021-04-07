##############################################################################
#
# Copyright (c) 2020 - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module HR_CRRAE
# ##############################################################################
{
    "name": "Rapports CRRAE",
    "version": "2.0",
    "author": "Rodolphe Agnero",
    'category': 'Localization',
    "website": "www.Rodolphe Agnero.net",
    "depends": ["base", "hr"],
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "wizards/hr_crrae_wizard.xml",
        "reports/report_view.xml",
        'security/ir.model.access.csv',
    ],
    "installable": True
}
