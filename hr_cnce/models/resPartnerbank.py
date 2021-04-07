# -*- coding:utf-8 -*-

from odoo import api, fields, models


class ResBank(models.Model):
    _inherit = "res.bank"

    partner_id = fields.Many2one('res.partner', 'Account Holder', ondelete='cascade', index=True,
                                 domain=['|', ('is_company', '=', True), ('parent_id', '=', False)], required=False)


class ResPartnerBank(models.Model):
    _inherit = "res.partner.bank"

    employee_id = fields.Many2one("hr.employee", "Titulaire", required= False)