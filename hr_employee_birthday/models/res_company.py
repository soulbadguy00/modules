#-*- coding:utf-8 -*-

from odoo import api, fields, models

class ResCompany(models.Model):
    _inherit = 'res.company'


    days_before_birthday= fields.Integer("Nombre de jours avant la date d'anniversaire", default=0, readonly=False)