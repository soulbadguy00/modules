##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_emprunt
# ##############################################################################
{
    "name" : "Congés automatiques",
    "version" : "1.0",
    "author" : "Rodolphe Agnero",
    "category" : "Human Resources",
    "website" : "www.Rodolphe Agnero.com",
    "depends" : ['hr_holidays_extension'],
    "description": """ Ce module permet d'attribuer de façon automatqiue les congés annuels des employés
    """,
    "init_xml" : [],
    "demo_xml" : [],
    "data": [
        'data/cron_view.xml',
        'views/res_config_settings_view.xml',
    ],
    "installable": True
}
