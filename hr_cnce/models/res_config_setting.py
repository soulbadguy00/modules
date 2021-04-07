# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    days_before_holidays = fields.Integer(string="Alerte depart congés (Jours)", readonly=False,
                                          related="company_id.days_before_holidays")
    days_after_holidays = fields.Integer(string="Alerte retour congés (Jours)", readonly=False,
                                         related="company_id.days_after_holidays")
    first_alert_retraite = fields.Integer(string="Première alerte depart retraite (Mois)", readonly=False,
                                          related="company_id.first_alert_retraite")
    second_alert_retraite = fields.Integer(string="Deuxième alerte depart retraite (Mois)", readonly=False,
                                         related="company_id.second_alert_retraite")
