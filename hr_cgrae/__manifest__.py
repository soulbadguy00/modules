##############################################################################
#
# Copyright (c) 2020 - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_cgrae
# ##############################################################################
{
    "name": "Rapports CGRAE",
    "version": "1.0",
    "author": "Rodolphe Agnero",
    'category': 'Localization',
    "website": "www.Rodolphe Agnero.net",
    "depends": ["base", "web", "hr", "hr_contract_extension","hr_payroll_ci","hr_payroll_ci_raport"],
    "init_xml": [],
    "demo_xml": [],
    "data": [
        "security/ir.model.access.csv",
        #"data/hr_salary_rule.xml",
        "reports/report_menu.xml",
        "views/report_hr_cgrae.xml",
        "views/ResCompanyView.xml",
        "views/hr_convention_view.xml",
        "views/hr_cgrae_export_wizard_view.xml",
        "views/report_cgrae_list.xml"
    ],
    "installable": True
}
