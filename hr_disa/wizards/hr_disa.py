# -*- coding:utf-8 -*-

from odoo import api, fields, _, models


import time
from datetime import datetime
from datetime import time as datetime_time
from dateutil import relativedelta

class HrDISA(models.TransientModel):
    _name ='hr.disa'
    _description = "Gestion des etats disa"

    date_from = fields.Date(string='Date From', required=True, default=time.strftime('%Y-01-01'))
    date_to = fields.Date(string='Date To', required=True, default=time.strftime('%Y-12-31'))
    company_id = fields.Many2one("res.company", "Société", default=lambda self: self.env.user.company_id.id)


    def computeDisa(self):
        res = []
        employees = self.env['hr.employee'].search([('company_id', '=', self.company_id.id)])
        if employees:
            num_order = 0
            for emp in employees:
                val = {
                    'order': num_order + 1,
                    'employee_name': str(emp.name) + ' ' + str(emp.first_name),
                    'num_cnps': emp.matricule_cnps,
                    'date_naissance': format(emp.birthday.strftime("%d/%m/%Y")) if emp.birthday else '',
                    'date_embauche': format(emp.start_date.strftime("%d/%m/%Y")) if emp.start_date else '',
                    'date_depart': format(emp.end_date.strftime("%d/%m/%Y")) if emp.end_date else '',
                    'type_employee': emp.type.upper() if emp.type else '',
                    'temps_travail': emp.getTotalRubriqueByPeriod('WORK100', self.date_from, self.date_to),
                    'brut_total': emp.getTotalRubriqueByPeriod('BRUT', self.date_from, self.date_to),
                    'brut_autre': emp.getAmountRubriqueByPeriod('BACT_PF', self.date_from, self.date_to),
                    'brut_cnps': emp.getAmountRubriqueByPeriod('CNPS', self.date_from, self.date_to),
                    'cotisation': '1234',
                    'comment': ""
                }
                res.append(val)
                num_order += 1
        return res


    def export_to_excel(self):
        for rec in self:
            data = {}
            context = rec.env.context
            rec.ensure_one()
            data['lines'] = rec.computeDisa()
            data['ids'] = rec.id
            data['model'] = rec._name
            return rec.env.ref('hr_disa.action_raport_hr_disa').report_action(rec, data=data)
