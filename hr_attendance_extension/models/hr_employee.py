# -*- coding:utf-8 -*-


from odoo import api, fields, models, exceptions
from itertools import groupby

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    overtime_ids= fields.One2many('hr.attendance.heure.supp', 'employee_id', "Heures supplémentaires")

    def getWorkInput(self, contract, date_from, date_to):
        res = []
        overtimes = self.getOvertime(contract.id, date_from, date_to)
        if overtimes :
            res+= overtimes
        return res


    def getOvertime(self, contract_id, date_start, date_end):
        res = []
        hstypes = self.env["hr.attendance.heure.supp.type"].search([])
        if hstypes:
            for type in hstypes:
                total = 0
                id_work_entry_type = self.env['hr.work.entry.type'].search([('code', '=', type.code)], limit=1).id
                dic = {
                    'work_entry_type_id': id_work_entry_type,
                    'code': type.code,
                    'number_of_hours': total,
                    'name': type.name,
                    'contract_id': contract_id
                }
                overtimes = self.env['hr.attendance.heure.supp'].search([]).filtered(lambda over : over.h_date >= date_start and over.h_date <= date_end
                     and over.state == 'confirmed' and over.heure_supp_type_id == type and over.employee_id.id == self.id)
                print(overtimes)
                if overtimes :
                    total = sum([over.nb_heure for over in overtimes])
                    dic['number_of_hours'] = total
                res.append(dic)
        return res

