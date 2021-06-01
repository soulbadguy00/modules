# -*- coding:utf-8 -*-


from odoo import api, models, fields, _


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    iban = fields.Char("IBAN")