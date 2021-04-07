# -*- coding:utf-8 -*-

from odoo import api, fields, models

class HrHolidays(models.Model):
    _inherit = 'hr.leave'

    def createHolidays(self, employee_id, number_of_days):
        type= self.env['hr.holidays.status'].search([('code', '=', 'CONG')], limit=1)
        if type:
            vals = {
                'holidays_type' : 'employee',
                'employee_id': employee_id,
                'holidays_status_id': type.id,
                'number_of_days_temps': number_of_days,
            }
            self.create(vals)



