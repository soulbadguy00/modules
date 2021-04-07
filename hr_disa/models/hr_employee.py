# -*- coding:utf-8 -*-

from odoo import api, models, fields

class HrEmployee(models.Model):
    _inherit = "hr.employee"

    def getTotalRubriqueByPeriod(self, code, date_from, date_to):
        amount = 0
        payslips = self.slip_ids.filtered(lambda slip: slip.date_from >= date_from and slip.date_to <= date_to)
        if payslips:
            p_lines = self.env['hr.payslip.line'].search([('code', '=', code), ('slip_id', 'in', payslips.ids)])
            if p_lines:
                amount = sum([line.total for line in p_lines])
        return amount

    def getAmountRubriqueByPeriod(self, code, date_from, date_to):
        amount = 0
        payslips = self.slip_ids.filtered(lambda slip: slip.date_from >= date_from and slip.date_to <= date_to)
        if payslips:
            p_lines = self.env['hr.payslip.line'].search([('code', '=', code), ('slip_id', 'in', payslips.ids)])
            if p_lines:
                amount = sum([line.amount for line in p_lines])
        return amount