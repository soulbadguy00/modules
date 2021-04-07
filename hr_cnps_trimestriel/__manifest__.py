# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name" : "CNPS Trimestrielle",
    "version" : "1.0",
    "author" : "Rodolphe Agnero Technologies",
    'category': 'Human Resources',
    "website" : "www.Rodolphe Agnero.net",
    "depends" : ['base', 'hr_payroll_ci_raport'],
    "description": """ 
    Gestion de la CNPS trimestrielle
    """,
    "init_xml" : [],
    "demo_xml" : [],
    "data":[
        "security/ir.model.access.csv",
        "wizard/HrCnpsTrimestrielView.xml",
        "reports/report_cnps_trimestriel.xml",
        "reports/report_menu.xml",
    ],
    "installable": True
}
