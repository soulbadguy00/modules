# -*- encoding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_emprunt
# ##############################################################################  -->
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import date

from odoo import fields, osv, models, api
from odoo.tools.translate import _
from odoo import netsvc


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    payment_method = fields.Selection([('espece', 'Espèces'), ('virement', 'Virement bancaire'), ('cheque', 'Chèques')],
                                      string='Moyens de paiement', required=True)
    piece_identite_id = fields.Many2one("hr.piece.identite", "Pièce d'identité")
    num_piece = fields.Char("Numéro de la pièce", required=False)
    type_piece_id = fields.Many2one('hr.employee.nature_piece', "Type de pièce", required=False)

    def getInputsPayroll(self, contract, date_from, date_to):
        res = []
        primes = contract.hr_payroll_prime_ids
        for prime in primes:
            if prime.prime_id.code == "TRSP":
                id_prime_transport = self.env['hr.payslip.input.type'].search([('code', '=', 'TRSP')], limit=1).id
                print("id_prime_transport", id_prime_transport)
                if prime.montant_prime > 30000:
                    montant_imp = prime.montant_prime - 30000
                    inputs = {
                        'name': "Prime de transport imposable",
                        'code': "TRSP_IMP",
                        'contract_id': contract.id,
                        'amount': montant_imp,
                        'input_type_id': id_prime_transport,
                    }
                    res += [inputs]
                    inputs = {
                        'name': prime.prime_id.name,
                        'code': prime.code,
                        'contract_id': contract.id,
                        'amount': 30000,
                        'input_type_id': id_prime_transport,
                    }
                    res += [inputs]
                else:
                    inputs = {
                        'name': prime.prime_id.name,
                        'code': prime.code,
                        'contract_id': contract.id,
                        'amount': prime.montant_prime,
                        'input_type_id': id_prime_transport,
                    }
                    res += [inputs]
            else:
                id_prime = self.env['hr.payslip.input.type'].search([('code', '=', prime.prime_id.code)], limit=1).id
                inputs = {
                    'name': prime.prime_id.name,
                    'code': prime.code,
                    'contract_id': contract.id,
                    'amount': prime.montant_prime,
                    'input_type_id': id_prime,
                }
                res += [inputs]
        return res


class HrEmployeeNaturePiece(models.Model):
    _name = "hr.employee.nature_piece"
    _description = "Nature de la piece"

    name = fields.Char("Libellé", required=True, size=225)
    description = fields.Text("Description", required=False)
