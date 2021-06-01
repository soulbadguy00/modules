# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountJournal(models.Model):
    _inherit = "sale.order"

    payment_method = fields.Selection([('espece', 'Espèces'), ('virement', 'Virement bancaire'), ('cheque', 'Chèques')],
                                      string='Moyens de paiement', required=True)
