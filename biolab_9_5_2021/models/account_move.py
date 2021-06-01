# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    payment_method = fields.Selection([('espece', 'Espèces'), ('virement', 'Virement bancaire'), ('cheque', 'Chèques')],
                                      string='Moyens de paiement', required=True)
    expiration_date = fields.Date('Date limite de règlement')
    cheque_label = fields.Char('Libellé chèque')
