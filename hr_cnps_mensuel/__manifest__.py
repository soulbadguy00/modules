# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name" : "CNPS Mensuel",
    "version" : "1.0",
    "author" : "Jean-Jonathan ARRA",
    'category': 'Human Resources',
    "website" : "",
    "depends" : ['base', 'hr_payroll_ci_raport'],
    "description": """ 
    Gestion de la CNPS mensuelle
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [

        ],
    "data": [
        "security/ir.model.access.csv",
        "data/hr_cnps_settings.xml",
        "views/hrCnpsSettingsView.xml",
        "views/hrCnpsMonthlyView.xml",
        "views/hrPayslipView.xml",
        "reports/report_cnps_monthly.xml",
        "reports/report_menu.xml",
    ],
    "installable": True
}
