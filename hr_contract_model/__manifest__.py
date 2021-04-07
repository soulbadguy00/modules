# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero Technologies
#
# Fichier du module hr_contract_model
# ##############################################################################
{
    'name': "Contracts Models",
    'version': "2.0",
    'author': "Rodolphe Agnero Technologies",
    'category': 'Human Resources',
    'website': "www.Rodolphe Agnero.net",
    'depends': ['base', 'hr_contract', 'hr_payroll', 'hr_contract_extension'],
    'description': """ 
        Gestion des modèles de contracts
    """,
    'data': [
            "security/ir.model.access.csv",
            "views/hr_contract_model_view.xml",
        ],
    'auto_install': False,
    'installable': True
}
