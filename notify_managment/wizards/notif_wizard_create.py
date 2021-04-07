# -*- coding:utf-8 -*-

from odoo import api, fields, api, _, models

class NotifWizardCreate(models.TransientModel):
    _name = 'notif.wizard.create'
    _description = "notif wizard create"

    notif_model_id = fields.Many2one('notify.model', 'Modèle de notification', required=True)


    def compute_notification(self):
        for rec in self:
            notif_model = rec.env['notif.line']
            model = rec.env[rec._context.get('active_model')].browse(rec._context.get('active_id'))
            print(model)