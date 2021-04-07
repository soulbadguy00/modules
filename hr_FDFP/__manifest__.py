# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name" : "DÉCLARATION FDFP",
    "version" : "1.0",
    "author" : "Rodolphe Agnero",
    'category': 'Human Resources',
    "website" : "www.Rodolphe Agnero.net",
    "depends" : ['base', 'hr_payroll_ci_raport'],
    "description": """ 
    Gestion de la déclaration FDFP
    """,
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/ir.model.access.csv",
        "reports/hr_report_menu.xml",
        "reports/report_hr_fdfp.xml",
        'views/hr_salary_rule_view.xml',
        "views/hr_fdfp_setting_view.xml",
        'views/hr_fdfp_view.xml',
    ],
    "installable": True
}
