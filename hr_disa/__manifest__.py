# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2020 KERYATEC - support@keryatec.com
# Author: Jean-Jonathan ARRA
#
# Fichier du module DISA
# ##############################################################################
{
    "name": "DISA",
    "version": "1.0",
    "author": "Keryatec",
    'category': 'Human Resources',
    "website": "www.keryatec.com",
    "depends": ["web","hr_payroll_ci_raport"],
    "description": """ 
        gestion des rapports DISA, DISA État 301, DISA État 302
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [
    ],
    "data": [
        "security/ir.model.access.csv",
        "raports/raport_menu.xml",
        "wizards/hr_disa_view.xml",
    ],
    "installable": True
}
