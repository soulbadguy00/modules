# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name": "Extension du contrats",
    "version": "1.0",
    "author": "Rodolphe Agnero Technologies",
    'category': 'Human Resources',
    "website": "www.Rodolphe Agnero.net",
    "depends": ['base', "hr_contract", 'hr_payroll', 'notify_managment', 'hr_update'],
    "description": """ 
    Extension du contrats de travail des employés
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [

        ],
    "data": [
           "security/ir.model.access.csv",
            "data/primes_data.xml",
            "wizard/hr_compute_inverse_view.xml",
            "views/hr_employee_view.xml",
            "views/hr_convention_view.xml",
            "views/hr_contract_view.xml",
            ],
    "installable": True
}


