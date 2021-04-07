# -*- coding:utf-8 -*-

from odoo import api, models, fields, _

class HrEmployeeSalaryDispatched(models.Model):
    _name = "hr.employee.salary.dispatched"
    _description = "hr employe salary dispatched"

    @api.model
    def _get_active_employee(self):
        print(self.env.context)

    name = fields.Char('Désignation', required=True)
    employee_id = fields.Many2one('hr.employee', "employé", required=True)
    #line_ids = fields.One2many('hr.employee.salary.dispatched.line', 'salary_dispatched_id', 'Lignes', required=True)
    active = fields.Boolean('Actif', default=True)


class HrEmployeeSalaryDispatchedLine(models.Model):
    _name = "hr.employee.salary.dispatched.line"
    _description = "hr employee salary dispatched line"

    bank_id = fields.Many2one('res.partner.bank', 'Compte bancaire', required=True)
    type = fields.Selection([('balance', 'Balance'), ('fix', 'Montant fix')], 'Type', default='balance')
    amount = fields.Integer('Montant', default=0)
    employee_id = fields.Many2one('hr.employee', "Employé", required=False)
    description = fields.Text("Commentaire", required=False)