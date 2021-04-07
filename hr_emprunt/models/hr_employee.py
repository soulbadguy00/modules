# -*- coding:utf-8 -*-


from odoo import api, fields, models, _
from datetime import date, datetime


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    loaning_ids = fields.One2many('hr.emprunt.loaning', 'employee_id', 'Écheanciers')
    demande_ids = fields.One2many('hr.emprunt.demande', 'employe_id', 'Demandes')

    def get_amount_emprunt(self, date_from, date_to):
        for rec in self:
            loaning_obj = rec.env['hr.emprunt.loaning']
            amount = 0
            if date_from and date_to:
                loanings = loaning_obj.search([('employee_id', '=', rec.id)])
                if loanings:
                    for loaning in loanings:
                        # print loaning.echeance_ids
                        echeances = loaning.echeance_ids.filtered(
                            lambda r: r.date_prevu <= date_to and r.date_prevu >= date_from)

                        if echeances:
                            amount = sum([ech.montant for ech in echeances])
            # print "mount total is %s" %amount
            return amount

    def getAdvancedSalaryMonthly(self, date_from, date_to):
        for rec in self:
            as_obj = rec.env['hr.advance.salary']
            amount = 0
            print('L34 avance sur salaire')
            if date_from and date_to:
                advance_salaries = as_obj.search([('employee_id', '=', rec.id)]).filtered(
                    lambda r: r.date <= date_to and r.date >= date_from)
                print('L37', advance_salaries)
                if advance_salaries:
                    amount = sum([ad.amount for ad in advance_salaries])
            return amount

    def getInputsPayroll(self, contract, date_from, date_to):
        for rec in self:
            res = super(HrEmployee, rec).getInputsPayroll(contract, date_from, date_to)
            avs = rec.getAdvancedSalaryMonthly(date_from, date_to)
            if avs != 0:
                id_avance_salaire = self.env['hr.payslip.input.type'].search([('code', '=', 'AVS')], limit=1).id
                val = {
                    'name': "Avance sur salaire",
                    'code': "AVS",
                    'amount': avs,
                    'contract_id': contract.id,
                    'input_type_id': id_avance_salaire,
                }
                res += [val]
            #emprunts = rec.get_amount_emprunt(date_from, date_to)
            #if emprunts != 0:
            id_employee = contract.employee_id.id
            echeances_rc = self.env['hr.emprunt.loaning'].search([('employee_id', '=', id_employee),
                                                                 ('remaining_emprunt', '<', 100),
                                                                 ('date_debut_remboursement', '<=', date.today())])
            print('L64 - echeance_rc',echeances_rc)
            if echeances_rc:
                for echeance_rc in echeances_rc:
                    id_emprunt = False
                    for loaning in echeance_rc.echeance_ids:
                        print('L69 ',type(date_from))
                        print('L70 ',type(date_to))
                        print('L71 ',type(loaning.date_prevu))
                        if date_from <= datetime.combine(loaning.date_prevu, datetime.min.time()) <= date_to:
                            id_emprunt = loaning.loaning_id
                            amount = loaning.montant
                            print('L70 - id_emprunt',id_emprunt)
                            break
                    if id_emprunt:
                        code_emprunt = id_emprunt.type_emprunt_id.code
                        print('L74',code_emprunt)

                    id_type_emprunt = self.env['hr.payslip.input.type'].search([('code', '=', code_emprunt)], limit=1)
                    val = {
                        'name': id_type_emprunt.name,
                        'code': id_type_emprunt.code,
                        'amount': amount,
                        'contract_id': contract.id,
                        'input_type_id': id_type_emprunt.id,
                    }
                    res += [val]
            print('L64', res)
            return res
