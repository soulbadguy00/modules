# -*- coding:utf-8 -*-

from odoo import api, models, fields, _
from odoo.exceptions import AccessError
from datetime import datetime


# from dateutils import rela


class Employee(models.Model):
    _inherit = "hr.employee"

    current_leave_state = fields.Selection(compute='_compute_leave_status', string="Current Leave Status",
                                           selection_add=[('technical', 'Technical'), ('not_technical', 'No Technical'),
                                                          ('chef_service', 'Chef de service'),
                                                          ('crh', 'Chargé des RH'),
                                                          ('chef_depart', 'Chef de departement'), ('cdaf', 'RAF'), ])
    date_return_last_holidays = fields.Date(compute='_compute_remaining_leaves_legals', string="Date de retour Congés",
                                            store=True)
    date_depart_holidays = fields.Date(compute='_compute_remaining_leaves_legals', string='Date de depart en congés')
    holidays_legal_leaves = fields.Float(compute='_compute_remaining_leaves_legals', string='Congés légaux restants')

    def _getDateHolidays(self):
        """Checks that choosen address (res.partner) is not linked to a company.
        """
        for rec in self:
            if rec:
                type_holiday = False
                try:
                    type_holiday = \
                    self.env['hr.leave.type'].search([('time_type', '=', 'leave'), ('code', '=', 'CONG')])[0]
                except:
                    print('error type_holiday')

                vals = {
                    'date_return_last_holidays': rec.start_date,
                    'date_depart_holidays': False
                }
                if type_holiday:

                    today = fields.Datetime.now()
                    holidays = rec.env['hr.leave'].search([('holiday_status_id', '=', type_holiday.id),
                                                           ('date_to', '<', today), ('employee_id', '=', rec.id)],
                                                          order="date_to desc", limit=1)
                    if holidays:
                        print(holidays.date_to)
                        vals['date_return_last_holidays'] = str(holidays.date_to)[:10]
                    holidays_next = rec.env['hr.leave'].search(
                        [('holiday_status_id', '=', type_holiday.id), ('date_from', '>', today),
                         ('employee_id', '=', rec.id)],
                        order="date_from", limit=1)
                    if holidays_next:
                        vals['date_depart_holidays'] = str(holidays_next.date_from)[:10]
                    return vals

    def _get_remaining_leaves(self):
        """ Helper to compute the remaining leaves for the current employees
            :returns dict where the key is the employee id, and the value is the remain leaves
        """
        for rec in self:
            if rec.ids:
                rec._cr.execute("""
                    SELECT
                        sum(h.number_of_days) AS days,
                        h.employee_id
                    FROM
                        (
                            SELECT holiday_status_id, number_of_days,
                                state, employee_id
                            FROM hr_leave_allocation
                            UNION
                            SELECT holiday_status_id, (number_of_days * -1) as number_of_days,
                                state, employee_id
                            FROM hr_leave
                        ) h
                        join hr_leave_type s ON (s.id=h.holiday_status_id)
                    WHERE
                        h.state='validate' AND
                        (s.allocation_type='fixed' OR s.allocation_type='fixed_allocation') AND
                        h.employee_id in %s
                    GROUP BY h.employee_id""", (tuple(rec.ids),))
                return dict((row['employee_id'], row['days']) for row in rec._cr.dictfetchall())

    def _compute_remaining_leaves_legals(self):
        for employee in self:
            employee.date_return_last_holidays = 0
            employee.date_depart_holidays = 0
            remaining = employee._get_remaining_leaves()
            if remaining:
                employee.holidays_legal_leaves = remaining.get(employee.id, 0.0)
                vals = employee._getDateHolidays()
                if vals:
                    employee.date_return_last_holidays = vals['date_return_last_holidays']
                    employee.date_depart_holidays = vals['date_depart_holidays']
