##############################################################################
#
# Copyright (c) 2020 - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_301
# ##############################################################################
{
    "name": "Rapports ETAT 301",
    "version": "1.0",
    "author": "Jean Jonathan ARRA",
    'category': 'hr',
    "website": "",
    "depends": ["base", "hr_payroll", "hr_payroll_ci_raport"],  # "account",
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_301_view.xml",
    ],
    "installable": True
}
