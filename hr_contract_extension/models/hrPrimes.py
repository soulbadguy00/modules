# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrPayrollPrime(models.Model):
    _name = "hr.payroll.prime"
    _description = "prime"

    name = fields.Char('name', size=64, required=True)
    code = fields.Char('Code', size=64, required=True)
    description = fields.Text('Description')


class HrPayrollPrimeAmount(models.Model):
    _name = "hr.payroll.prime.montant"
    _description = "Primes management"


    @api.depends('prime_id')
    def _get_code_prime(self):
        for rec in self:
            if rec.prime_id:
                rec.code = rec.prime_id.code

    prime_id = fields.Many2one('hr.payroll.prime', 'prime', required=True)
    code = fields.Char("Code", compute='_get_code_prime')
    contract_id = fields.Many2one('hr.contract', 'Contract')
    montant_prime = fields.Integer('Montant', required=True)
