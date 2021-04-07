#-*- coding-utf-8 -*-
{
    'name': "Base de gestion des modèles de notification",
    'summary': """
    Modèle de gestion des notification.
       """,
    'author': 'Rodolphe Agnero',
    'company': 'Rodolphe Agnero',
    'website': 'http://www.rodolpheagnero.com',
    'category': 'Tools',
    'version': '2.0',
    'license': 'AGPL-3',
    'depends': [
        'base',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/notify_managment_view.xml',
        'wizards/notifWizardCreateView.xml',
    ],
}
