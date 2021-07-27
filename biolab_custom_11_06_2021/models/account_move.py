# -*- coding:utf-8 -*-


from odoo import api, models, fields, _
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    def _getAmountToText(self):
        for move in self:
            amount_text = num2words(move.amount_total, lang='fr')
            move.amount_text = amount_text

    num_bdl = fields.Char("BDL", required=False)
    amount_text = fields.Char("Montant en lettres", compute="_getAmountToText")
    partner_contact_id = fields.Many2one('res.partner', "Contact", domain="[('type', '=', 'ocntact')]")

