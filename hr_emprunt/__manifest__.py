##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_emprunt
# ##############################################################################
{
    'name': 'Emprunt',
    'version' : '14.0.1.0.0',
    'author': 'Rodolphe Agnero',
    'category': 'Generic Modules/Human Resources',
    'website': 'www.Rodolphe Agnero.net',
'depends': ['hr', 'mail', 'hr_payroll'],
    'description': """ Module permettant de gérer les emprunts des employés 
(Echeanciers, Remboursement, interfaçage avec le module de paie)
    """,
    "demo": [],
    "data": [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/hr_emprunt_view.xml',
        'views/report_hr_emprunt.xml',
        #'report/report.xml',
        'views/hr_demande_emprunt_view.xml',
        'views/hr_advance_salary_view.xml',
        'email/notification_email.xml',
    ],
    'licence': 'LGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False
}
