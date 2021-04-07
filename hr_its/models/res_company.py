# -*- coding:utf-8 -*-

from odoo import api, fields, _, models


class ResCompany(models.Model):
    _inherit = "res.company"

    rate_ce_local = fields.Float("Taux CE employés locaux", default=0)
    rate_ce_expat = fields.Float("Taux CE employés expat", default=11.5)
    rate_ce_agricole = fields.Float("Taux employeur Régime agricole", default=2)
    rate_its = fields.Float("Taux ITS", default=1.5)