# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
from dateutil import relativedelta


class NotifModel(models.Model):
    _name = 'notify.model'
    _description = "Notify model"

    name = fields.Char("Libellé", required=True, size=255)
    line_ids = fields.One2many('notify.model.line', 'notif_id', 'Lignes', required=True)

    def getNotifLine(self, date_fin):
        res = []
        for line in self.line_ids:
            if line.type == 'an':
                date = str(date_fin + relativedelta.relativedelta(years=-line.number))
            elif line.type == 'mois':
                date = str(date_fin + relativedelta.relativedelta(months=-line.number))
            elif line.type == 'day':
                date = str(date_fin + relativedelta.relativedelta(days=-line.number))
            else:
                date = str(date_fin + relativedelta.relativedelta(hours=-line.number))
            val = {
                'date_notification': date,
            }
            res.append(val)
        return res


class NotifModelLine(models.Model):
    _name = 'notify.model.line'
    _description = "Notify line model managment"

    type = fields.Selection([('an', 'Année'), ('mois', 'Mois'), ('day', 'Jours'), ('hours', 'Heures')], string="Type",
                            required=True)
    number = fields.Integer('Date', required=True, default=1)
    notif_id = fields.Many2one('notify.model', 'Notif')


class NotifLine(models.Model):
    _name = 'notif.line'
    _description = "Gestion des notification"

    def generate_notification_line(self, res_model, res_id, line, date_fin):
        if res_model and res_id and line:
            if line.type == 'an':
                date = str(date_fin + relativedelta.relativedelta(years=-line.number))
            elif line.type == 'mois':
                date = str(date_fin + relativedelta.relativedelta(months=-line.number))
            elif line.type == 'day':
                date = str(date_fin + relativedelta.relativedelta(days=-line.number))
            else:
                date = str(date_fin + relativedelta.relativedelta(hours=-line.number))
            val = {
                'res_model': res_model,
                'res_id': res_id,
                'date_notifcation': date,
            }
            self.create(val)

    res_model = fields.Char('Modèle', required=True)
    res_id = fields.Integer('ID modèle', required=True)
    date_notifcation = fields.Datetime('Date de notification')
    active = fields.Boolean('Active', default=True)
