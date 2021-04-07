# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import api, fields, models


class HrPayrollReport(models.Model):
    _name = "hr.payroll.report"
    _description = "Payroll Analysis Report"
    _auto = False
    _rec_name = 'date_from'
    _order = 'date_from desc'

    name = fields.Char('Payslip Name', readonly=True)
    category_id = fields.Many2one("hr.contract.category", "Catégorie", readonly=True)
    date_from = fields.Date('Start Date', readonly=True)
    date_to = fields.Date('End Date', readonly=True)
    company_id = fields.Many2one('res.company', 'Company', readonly=True)

    employee_id = fields.Many2one('hr.employee', 'Employee', readonly=True)
    direction_id = fields.Many2one('hr.department', 'Direction', readonly=True)
    department_id = fields.Many2one('hr.department', 'Departement', readonly=True)
    service_id = fields.Many2one('hr.department', 'Service', readonly=True)
    job_id = fields.Many2one('hr.job', 'Job Position', readonly=True)
    agence_id = fields.Many2one('hr.agence', 'Agence', readonly=True)
    net = fields.Float('Net', readonly=True)
    brut_imposable = fields.Float('Brut imposable', readonly=True)
    brut_total = fields.Float('Brut total', readonly=True)

    def init(self):
        query = """
            SELECT
                p.id as id,
                p.name as name,
                p.date_from as date_from,
                p.date_to as date_to,
                e.id as employee_id,
                e.direction_id as direction_id,
                e.department_id as department_id,
                e.service_id as service_id,
                e.agence_id as agence_id,
                e.category_id as category_id,
                e.job_id as job_id,
                e.company_id as company_id,
                pln.total as net,
                plb.total as brut_imposable,
                plbt.total as brut_total
            FROM
                (SELECT * FROM hr_payslip WHERE state IN ('draft', 'done', 'paid')) p
                    left join hr_employee e on (p.employee_id = e.id)
                    left join hr_payslip_line pln on (pln.slip_id = p.id and  pln.code = 'NET')
                    left join hr_payslip_line plb on (plb.slip_id = p.id and plb.code = 'BRUT')
                    left join hr_payslip_line plbt on (plbt.slip_id = p.id and plbt.code = 'BRUT_TOTAL')
            GROUP BY
                e.id,
                e.direction_id,
                e.service_id,
                e.department_id,
                e.agence_id,
                e.company_id,
                p.id,
                p.name,
                p.date_from,
                p.date_to,
                pln.total,
                plb.total,
                plbt.total
                """
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute("""CREATE or REPLACE VIEW %s as (%s)""" % (self._table, query))
