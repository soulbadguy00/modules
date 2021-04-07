# -*- coding: utf-8 -*-
###################################################################################

#
###################################################################################
{
    'name': 'HR Jobs history',
    'version': '14.0.1.0.0',
    'summary': """Manages Employee jobs history.""",
    'category': 'HR',
    'author': 'Rodolphe Agnero',
    'company': 'Rodolphe Agnero',
    'maintainer': 'Rodolphe Agnero',
    'website': "https://www.Rodolphe Agnero.net",
    'depends': ['base', 'hr', 'hr_contract'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_history_job_employee_view.xml',
        'views/hr_employee_view.xml'
    ],
    #'images': ['static/description/banner.jpg'],
    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': False,
}
