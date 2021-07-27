# -* coding:utf-8 -*-


from odoo import api, models, fields, _
from num2words import num2words


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _getAmountToText(self):
        for move in self:
            amount_text = num2words(move.amount_total, lang='fr')
            move.amount_text = amount_text

    object = fields.Char("Object", required=False)
    amount_text = fields.Char("Montant en lettres", compute="_getAmountToText")
    partner_contact_id = fields.Many2one('res.partner', "Contact", domain="[('type', '=', 'ocntact')]")
    date_end = fields.Date("Date de fin", required=False)
    partner_bank_id = fields.Many2one('res.partner.bank', string='Recipient Bank', help='Bank Account Number to which'
                    ' the invoice will be paid. A Company bank account if this is a Customer Invoice or Vendor Credit '
                    'Note, otherwise a Partner bank account number.',  check_company=True)


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        res = super()._prepare_invoice_values(order, name, amount, so_line)
        res["object"] = order.object
        return res

