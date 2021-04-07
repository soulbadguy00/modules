{
    "name": "Les Rapports  de paie",
    "version": "1.0",
    "depends": ['base','web','hr',"hr_payroll_ci", 'report_xlsx'],
    "author": "Rodolphe Agnero Team",
    "category": "hr",
    "description": """
    This module provide :
    """,
    'data': [
        'security/ir.model.access.csv',
        'views/asset_backend.xml',
        'data/report_templates.xml',
        "views/hr_rapport_menu.xml",
        "raports/payroll_raport.xml",
        "views/res_config_settings_views.xml",
        'wizard/HrPayrollView.xml',
        'views/HrSalaryRuleView.xml',
        'views/report_payroll.xml',
        'views/hr_payslip_view.xml',
        'views/hr_analyse_view.xml',
        "data/report_paperformat.xml",
    ],
    'demo_xml': [],
    'installable': True,
    'active': False,
}
