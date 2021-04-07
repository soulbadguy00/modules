# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrPayslipRun(models.Model):
    _inherit = "hr.payslip.run"

    state = fields.Selection(selection_add=[('in_progress', 'En cours de validation'), ('rejected', 'Rejeté')])


    def submit_to_validation(self):
        for run in self:
            run.state = "in_progress"


    def action_rejected(self):
        for run in self:
            run.state = "rejected"