# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    days_before_birthday = fields.Integer("Nombre de jours avant la date d'anniversaire", related="company_id.days_before_birthday", readonly=False)
