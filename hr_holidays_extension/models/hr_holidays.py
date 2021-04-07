# -*- coding:utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import Warning, ValidationError
from collections import namedtuple
from calendar import monthrange
from datetime import datetime

from odoo.tools import float_compare
from odoo.tools.float_utils import float_round

from dateutil.relativedelta import relativedelta


class hr_holidays(models.Model):
    _inherit = 'hr.leave'

    code = fields.Char('Code', size=4, required=False, related='holiday_status_id.code', store=True)
    number_due = fields.Integer("Nombre max dus", related="holiday_status_id.nbre_jr_max")
    date_payment = fields.Date("Date de prise en compte dans la paie")
    subtract_worked_days = fields.Boolean("À déduire des jours travaillés")

    @api.onchange('date_from', 'date_to', 'employee_id')
    def _onchange_leave_dates(self):
        number_of_days = 0
        if self.date_from and self.date_to:
            if self.holiday_status_id.is_calendar:
                date_from = fields.Datetime.from_string(self.date_from)
                date_end = fields.Datetime.from_string(self.date_to)
                tmp = date_end - date_from
                number_of_days = tmp.days
            else:
                number_of_days = self._get_number_of_days(self.date_from, self.date_to, self.employee_id.id)
        if number_of_days:
            self.number_of_days = number_of_days

    @api.model
    def computeHoldaysByType(self, date_from, date_to, contract, employee_id):
        res = []
        Range = namedtuple('Range', ['start', 'end'])
        hstatus = self.env['hr.holidays.status'].search([])
        r1 = Range(start=date_from, end=date_to)
        self._cr.execute("SELECT id FROM hr_holidays WHERE ((date_from"
                         " between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')) OR (date_to"
                         " between to_date(%s,'yyyy-mm-dd') AND to_date(%s,'yyyy-mm-dd')))"
                         " AND state='validate' AND payslip_status = TRUE  AND type='remove' AND employee_id='%s'",
                         (str(date_from), str(date_to),
                          str(date_from), str(date_to), employee_id))
        holidays_ids = [x[0] for x in self._cr.fetchall()]
        if holidays_ids:
            holidays = self.browse(holidays_ids)
            print(holidays)
            for status in hstatus:
                days = 0
                temp = holidays.filtered(lambda r: r.holiday_status_id == status)
                for tp in temp:
                    print(tp.date_from)
                    old_date_from = datetime.strptime(tp.date_from[:10], '%Y-%m-%d')
                    old_date_to = datetime.strptime(tp.date_to[:10], '%Y-%m-%d')
                    r2 = Range(start=old_date_from, end=old_date_to)
                    result = (min(r1.end, r2.end) - max(r1.start, r2.start)).days + 1
                    if result > 0:
                        days += result
                if days != 0:
                    nb_days = monthrange(date_from.year, date_from.month)
                    if days == nb_days[1]:
                        days = 30
                    hours = days * 173.33 / 30
                    vals = {
                        'name': status.name,
                        'sequence': 5,
                        'code': status.code,
                        'number_of_days': days,
                        'number_of_hours': hours,
                        'contract_id': contract.id,

                    }
                    res += [vals]
        return res

    @api.constrains('state', 'number_of_days', 'holiday_status_id')
    def _check_holidays(self):
        for holiday in self:
            if holiday.holiday_type != 'employee' or not holiday.employee_id or \
                    holiday.holiday_status_id.allocation_type == 'no':
                continue
            if holiday.holiday_status_id.allocation_type == 'legal':
                if holiday.number_due != holiday.number_of_days and holiday.number_due != 0:
                    raise Warning(_("Le nombre de jours pris ne correspond pas au nombre de jours définis par la "
                                    "réglémentoin en vigueur"))
                else:
                    continue
            else:
                leave_days = holiday.holiday_status_id.get_days(holiday.employee_id.id)[holiday.holiday_status_id.id]
                if float_compare(leave_days['remaining_leaves'], 0, precision_digits=2) == -1 or \
                        float_compare(leave_days['virtual_remaining_leaves'], 0, precision_digits=2) == -1:
                    raise ValidationError(_('The number of remaining leaves is not sufficient for this leave type.\n'
                                            'Please also check the leaves waiting for validation.'))


class HrHolidaysStatus(models.Model):
    _inherit = 'hr.leave.type'

    code = fields.Char('Code', size=4, required=False)
    nbre_jr_max = fields.Integer('Nombre de Jours(Max)')
    is_calendar = fields.Boolean('Basé sur les jours calendaires', default=True)
    allocation_type = fields.Selection(selection_add=[('legal', "Fixé par la réglementation en vigueur")])

    # holidays_category = fields.Selection([('leave', 'Absence'), ('holiday', 'Congé')], string='Catégorie')

    def name_get(self):
        if not self._context.get('employee_id'):
            # leave counts is based on employee_id, would be inaccurate if not based on correct employee
            return super(HrHolidaysStatus, self).name_get()
        res = []
        for record in self:
            name = record.name
            if record.allocation_type not in ('no', 'legal'):
                name = "%(name)s (%(count)s)" % {
                    'name': name,
                    'count': _('%g remaining out of %g') % (
                        float_round(record.virtual_remaining_leaves, precision_digits=2) or 0.0,
                        float_round(record.max_leaves, precision_digits=2) or 0.0,
                    ) + (_(' hours') if record.request_unit == 'hour' else _(' days'))
                }
            res.append((record.id, name))
        return res
