# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2020 Jean-Jonathan ARRA - jonathan.arra@gmail.com
# Author: Jean-Jonathan ARRA
#
# Fichier du module Recapitulatif des salaires
# ##############################################################################
{
    "name": "Recapitulatif des salaires",
    "version": "2.0",
    "author": "Rodolphe Agnero",
    'category': 'Human Resources',
    "depends": ["web", "hr_payroll_ci_raport"],
    "description": """ 
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hr_salary_employee_variation.xml",
        "reports/report_menu.xml",
        "wizards/hr_salary_variation.xml",
    ],
    "installable": True
}
