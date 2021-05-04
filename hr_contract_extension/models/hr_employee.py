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

    contract_ids = fields.One2many('hr.contract', 'employee_id', string='Contracts')
    contract_id = fields.Many2one('hr.contract', compute='_compute_contract_id', string='Current Contract',
                                  help='Latest contract of the employee')
    contracts_count = fields.Integer(compute='_compute_contracts_count', string='Contract Count')

    def _compute_contract_id(self):
        """ get the lastest contract """
        Contract = self.env['hr.contract']
        for employee in self:
            employee.contract_id = Contract.search([('employee_id', '=', employee.id)], order='date_start desc',
                                                   limit=1)

    def _compute_contracts_count(self):
        # read_group as sudo, since contract count is displayed on form view
        contract_data = self.env['hr.contract'].sudo().read_group([('employee_id', 'in', self.ids)], ['employee_id'],
                                                                  ['employee_id'])
        result = dict((data['employee_id'][0], data['employee_id_count']) for data in contract_data)
        for employee in self:
            employee.contracts_count = result.get(employee.id, 0)


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
