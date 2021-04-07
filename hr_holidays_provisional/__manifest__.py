# -*- coding:utf-8 -*-

{
    "name" : "Congés prévisionnels",
    "version" : "1.0",
    "author" : "Rodolphe Agnero",
    'category': 'Localization',
    "website" : "www.Rodolphe Agnero.net",
    "depends" : ["base","hr_holidays"],
    "description": """
     """,
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
        'data/email_template.xml',
        'security/ir.model.access.csv',
        'views/hr_holidays_view.xml',
    ],
    "data":[],
    "installable": True
}

