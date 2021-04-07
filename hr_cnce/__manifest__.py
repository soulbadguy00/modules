##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - jonathan.arra@gmail.com
# Author: Jean Jonathan ARRA
#
# Fichier du module hr_synthese
# ##############################################################################
{
    "name": "Update HR CNCE",
    "version": "2.0",
    "author": "Rodolphe Agnero",
    'category': 'Localization',
    "website": "http://www.rodolpheagnero.com",
    "depends": ['base', 'web', 'hr', 'hr_update', 'hr_contract_extension', 'hr_holidays', 'hr_holidays_extension',
                'hr_holidays_auto'],
    "description": """
    """,
    "init_xml": [],
    "demo_xml": [],
    "update_xml": [],
    "data": [
        "security/groups.xml",
        "security/ir.model.access.csv",
        "views/hrEmployeeSalaryDispatchedView.xml",
        "data/holidays_email_departement_template.xml",
        "data/holidays_email_director_template.xml",
        "data/holidays_email_template.xml",
        "data/holidays_email_template_first.xml",
        "data/holidays_email_validation_template.xml",
        "wizards/hr_holidays_wizard_view.xml",
        "views/HrLeavesView.xml",
        "views/hrHolidaysProvisionsView.xml",
        "views/hrHolidaysRecoveryView.xml",
        "views/hrHolidaysPlanningView.xml",
        "views/resBankView.xml",
        "views/hrContractView.xml",
        "views/hr_employee_view.xml",
        "views/resCompanyView.xml",
        "views/res_config_settings_views.xml",
        "views/hrLeavesForecastView.xml",
        "views/hr_payslip_view.xml",
        "views/hr_payslip_raport_view.xml",
        "reports/templates/layout_view.xml",
        "reports/report_view.xml",
        "reports/report_attestation_travail.xml",
        "reports/report_hr_holidays.xml",
        "reports/report_hr_holidays_recovery.xml",
    ],
    "installable": True
}
