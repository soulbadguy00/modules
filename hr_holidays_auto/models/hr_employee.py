# -*- coding:utf-8 -*-

from odoo import fields, api, models, _
from dateutil import relativedelta
from datetime import date

class hrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.model
    def compute_holidays_auto(self):
        this_date = date.today()
        type = self.env['hr.leave.type'].search([('code', '=', 'CONG')], limit=1)
        if type:
            for emp in self.search([]):
                if emp.start_date:
                    temp_date = fields.Date.from_string(emp.start_date) + relativedelta.relativedelta(month=this_date.month,
                                                                                                  year=this_date.year)
                    if temp_date == this_date:
                        print("Employé %s est venu le %s", (emp.name, emp.start_date))
                        vals = {
                            'holidays_type': 'employee',
                            'employee_id': emp.id,
                            'holiday_status_id': type.id,
                            'type': 'add'
                        }
                        if emp.nature_employe == 'local':
                            vals['number_of_days'] = emp.company_id.number_holidays_locaux
                        else:
                            vals['number_of_days'] = emp.company_id.number_holidays_expat
                        holidays = self.env['hr.leave.allocation'].create(vals)
                        if holidays:
                            holidays.action_validate()
        return True

    @api.model
    def compute_holidays_anciennete_auto(self):
        this_date = date.today()
        type = self.env['hr.leave.type'].search([('code', '=', 'CONG')], limit=1)
        if type:
            for emp in self.search([]):
                vals = {
                    'holidays_type': 'employee',
                    'employee_id': emp.id,
                    'holiday_status_id': type.id,
                    'type': 'add'
                }
                temp_date = fields.Date.from_string(emp.start_date) + relativedelta.relativedelta(year=this_date.year)
                if emp.start_date and this_date == temp_date:
                    tmp = relativedelta(this_date, temp_date)
                    if tmp.years >= 5 and tmp.year < 10:
                        vals['number_of_days'] = 1
                    elif tmp.years >= 10 and tmp.year < 15:
                        vals['number_of_days'] = 2
                    elif tmp.years >= 15 and tmp.year < 20:
                        vals['number_of_days'] = 3
                    elif tmp.years >= 20 and tmp.year < 25:
                        vals['number_of_days'] = 5
                    else:
                        if tmp.years  >= 25 :
                            vals['number_of_days'] = 7
                holidays = self.env['hr.leave.allocation'].create(vals)
                if holidays:
                    holidays.action_validate()
        return True


    def _get_date_compute_holidays(self):
        this_date = date.today()
        for emp in self:
            date_compute_holidays = fields.Date.from_string(emp.start_date) + relativedelta.relativedelta(year=this_date.year)
            emp.date_compute_holidays = date_compute_holidays

    date_compute_holidays = fields.Date("Date attribution allocation", compute="_get_date_compute_holidays")