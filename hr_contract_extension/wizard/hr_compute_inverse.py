# -*- coding:utf-8 -*-


import time
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, exceptions


class HrReverseContract(models.TransientModel):
    _name = 'hr.reverse.contract'
    _description = 'hr reverse contract'

    type_calcul = fields.Selection([('brut', 'Par le brut'), ('net', 'Par le net')], 'Méthode de calcul', required=True)
    montant = fields.Integer("Montant ")
    contract_id = fields.Many2one('hr.contract', 'Contrat')
    payslip = fields.Many2one('hr.payslip', 'Bulletin de paie')

    def compute(self):
        print('L20 ', self)
        for rec in self:
            print('compute in contract')
            # payslip_obj = rec.pool.get('hr.payslip')
            payslip_obj = rec.env['hr.payslip']
            total_intrant = rec.contract_id.wage
            print('L23-total_intrant ', total_intrant)
            # total_intrant = 200000
            sursalaire = 0
            for prime in rec.contract_id.hr_payroll_prime_ids:
                total_intrant += prime.montant_prime
            print('L28 ', total_intrant)
            if total_intrant > rec.montant:
                raise exceptions.ValidationError('Le montant est inféreur aux intrants')
            else:
                print('L32 ', rec.contract_id)
                structure_salariale = rec.contract_id.struct_id
                print('L33 ', structure_salariale)
                use_anc = False

                now = datetime.now()
                date_from = datetime(now.year, now.month, 1)
                date_to = date_from + relativedelta(months=1, days=-1)

                inputs = payslip_obj.get_inputs(rec.contract_id, date_from, date_to)
                input_line_ids = []
                if inputs:
                    for input in inputs:
                        temp = [0, False, input]
                        input_line_ids += [temp]
                worked_days = payslip_obj.get_worked_day_lines(rec.contract_id, date_from, date_to)
                worked_days_line_ids = []
                if worked_days:
                    for worked_day in worked_days:
                        temp = [0, False, worked_day]
                        worked_days_line_ids += [temp]
                vals = {
                    'name': "Salary Slip of " + rec.contract_id.employee_id.name,
                    'employee_id': rec.contract_id.employee_id.id,
                    'date_from': date_from,
                    'date_to': date_to,
                    'contract_id': rec.contract_id.id,
                    'struct_id': rec.contract_id.struct_id.id,
                    'input_line_ids': input_line_ids,
                    'worked_days_line_ids': worked_days_line_ids,
                }
                payslip_id = payslip_obj.create(vals)
                payslip_id.compute_sheet()
                if rec.type_calcul == 'brut':
                    for rule in structure_salariale.rule_ids:
                        if rule.code == 'PANC':
                            use_anc = True
                    print('use_anc ', use_anc)
                    if use_anc:
                        prime_anciennete = 0.0
                        if 1 < rec.contract_id.an_anciennete < 26:
                            prime_anciennete = 0.01 * rec.contract_id.wage * rec.contract_id.an_anciennete
                            total_intrant += prime_anciennete
                    brut_add = rec.montant - total_intrant
                    brut_amount = payslip_id.get_brut_amount()
                    while brut_amount != rec.montant:
                        if brut_amount < rec.montant:
                            brut_add += rec.montant - brut_amount
                        elif brut_amount > rec.montant:
                            brut_add -= (brut_amount - rec.montant)
                        rec.contract_id.sursalaire = brut_add
                        payslip_id.compute_sheet()
                        brut_amount = payslip_id.get_brut_amount()

                elif rec.type_calcul == 'net':
                    net_amount = payslip_id.get_net_paye()
                    while net_amount != rec.montant:
                        net_amount = payslip_id.get_net_paye()
                        if net_amount < rec.montant:
                            sursalaire += rec.montant - net_amount
                        elif net_amount > rec.montant:
                            sursalaire -= net_amount - rec.montant
                        rec.contract_id.sursalaire = sursalaire
                        payslip_id.compute_sheet()
            # else:
            #     sursalaire = rec.montant - total_intrant
            #     rec.contract_id.sursalaire = sursalaire
            break


__author__ = 'lekaizen'
