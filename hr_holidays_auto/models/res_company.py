# -*- coding:utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'

    number_holidays_locaux= fields.Float('Nombre de jours de congés mensuels à attribuer employé nationaux', default='2.2')
    number_holidays_expat = fields.Float('Nombre de jours de congés mensuels à attribuer employé expatriés', default='5')