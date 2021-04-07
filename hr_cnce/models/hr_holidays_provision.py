# -*- coding:utf-8 -*-

from odoo import api, fields, _, models
from dateutil import relativedelta


class HrHolidaysProvision(models.Model):
    _name = "hr.holidays.provision"
    _description = "hr holidays provision"

    name = fields.Char("Libellé", required=True, size=225)
    type = fields.Selection([('employee', 'Par employé'), ('all', 'Tous les employés')], 'Type de calcul', default="all")
    date_end = fields.Date("Date de fin", required=True)
    employee_id = fields.Many2one("hr.employee", 'Employé', required=False)
    line_ids = fields.One2many('hr.holidays.provision.line', 'hr_provision_id', 'Lignes')
    company_id = fields.Many2one('res.company', "Société", default=lambda self: self.env.user.company_id.id)

    def compute(self):
        for rec in self:
            for provision in rec:
                provision.line_ids.unlink()
                res = []

                if provision.type == 'employee':
                    facteur = provision.company_id.number_holidays_locaux if provision.employee_id.nature_employe == 'local' \
                        else provision.company_id.number_holidays_expat
                    tmp = provision.date_end - provision.employee_id.date_return_last_holidays
                    number_holidays = tmp.days * 12 / 360 * facteur
                    vals = {
                        "employee_id": provision.employee_id.id,
                        # "date_start": emp.date_return_last_holidays,
                        "date_start": provision.employee_id.date_return_last_holidays,
                        "date_end": provision.date_end,
                        "number_holidays": number_holidays
                    }
                    res.append(vals)
                else:
                    employees = rec.env['hr.employee'].search([])
                    if employees:
                        for emp in employees:
                            facteur = provision.company_id.number_holidays_locaux if emp.nature_employe == 'local' \
                                else provision.company_id.number_holidays_expat
                            if provision.date_end and emp.date_return_last_holidays:
                                tmp = provision.date_end - emp.date_return_last_holidays
                                number_holidays = tmp.days * 12/360 * facteur
                                vals = {
                                    "employee_id": emp.id,
                                    "date_start": emp.date_return_last_holidays,
                                    "date_end": provision.date_end,
                                    "number_holidays": number_holidays
                                }
                                print(vals)
                                res.append(vals)
                provision.update({"line_ids": res})


class HrHolidaysProvisinLine(models.Model):
    _name = "hr.holidays.provision.line"
    _description = "hr holidays provision line"

    employee_id = fields.Many2one("hr.employee", required=True)
    date_start = fields.Date("Date de retour congés")
    date_end = fields.Date("Date de fin", required=True)
    number_holidays = fields.Float("Nombre de jours de congés", digits=(10,2))
    hr_provision_id = fields.Many2one("hr.holidays.provision", "Parent", required=False)