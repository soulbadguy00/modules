# -*- coding:utf-8 -*-

from odoo import api, fields, _, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    @api.model
    def _get_tranche(self):
        type = 'm'
        for rec in self:
            if rec.employee_id:
                if rec.employee_id.type != 'm':
                    tranches = rec.env['hr.cnps.setting'].search([('type', '=', 'j')])
                    rec.env.cr.execute("SELECT amount FROM hr_payslip_line WHERE code = 'BASE' AND slip_id = %s" % (rec.id))
                    result = rec.env.cr.fetchone()
                    print('L18', result)
                    if tranches:
                        for tranche in tranches:
                            if result:
                                if result[0] >= tranche.amount_min and result[0] <= tranche.amount_max:
                                    rec.tranche_id = tranche.id
                else:
                    tranches = rec.env['hr.cnps.setting'].search([('type', '=', 'm')])
                    rec.env.cr.execute("SELECT total FROM hr_payslip_line WHERE code = 'BASE' AND slip_id = %s"%(rec.id))
                    result = rec.env.cr.fetchone()
                    print('L28', result)
                    if tranches:
                        for tranche in tranches:
                            if result:
                                if result[0] >= tranche.amount_min and result[0] <= tranche.amount_max:
                                    rec.tranche_id = tranche.id

                    print(result)
                    #result = self.env['hr.cnps.setting'].search([('type', '=', '')])

    tranche_id = fields.Many2one('hr.cnps.setting', 'Tranche', compute='_get_tranche', store=True)