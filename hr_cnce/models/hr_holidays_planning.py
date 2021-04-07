# -*- coding:utf-8 -*-

from odoo import api, fields, _, models
from odoo.exceptions import  Warning, ValidationError
from dateutil import relativedelta


class HrHolidaysPlanning(models.Model):
    _name = "hr.holiday.planning"
    _description = "HR Holidays Planning"

    def _default_employee(self):
        return self.env.context.get('default_employee_id') or self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)

    name = fields.Char("Libellé", required=True, size=225)
    employee_id = fields.Many2one("hr.employee", 'Employé', required=False, default=_default_employee)
    date_from = fields.Date("Début", required=True)
    date_end = fields.Date("Date de fin", required=True)
    number_of_days = fields.Float("Nombre jours")
    number_of_days_allocate = fields.Float("Nombre de jours attribués")
    company_id = fields.Many2one('res.company', "Société", default=lambda self: self.env.user.company_id.id)
    direction_id = fields.Many2one("hr.department", "Direction", related="employee_id.direction_id")
    department_id = fields.Many2one("hr.department", "Departement", related="employee_id.department_id")
    service_id = fields.Many2one("hr.department", "Service", related="employee_id.service_id")
    state = fields.Selection([('draft', "Brouillon"), ('wait', "En attente de validation"), ('done', 'Validé'),
                              ('cancel', "Annulé"), ('reject', 'Rejetté')], 'Statut', default='draft')

    @api.onchange('date_from', 'date_end')
    @api.depends('date_from', 'date_end')
    def _get_number_of_days(self):
        if self.date_from and self.date_end:
            facteur = self.company_id.number_holidays_locaux if self.employee_id.nature_employe == 'local' \
                else self.company_id.number_holidays_expat
            tmp = self.date_from - self.employee_id.date_return_last_holidays
            number_holidays = tmp.days * 12 / 360 * facteur
            self.number_of_days_allocate = number_holidays
            temp = self.date_end - self.date_from
            self.number_of_days = temp.days



    def action_submit(self):
        who_notified = False
        for rec in self:
            if self.employee_id.type_employee == 'employee' :
                if self.service_id :
                    who_notified = 'service'
                elif self.department_id :
                    who_notified = 'department'
                else :
                    who_notified = 'direction'
            elif self.employee_id.type_employee == 'chief_service':
                if self.department_id :
                    who_notified = 'department'
                else :
                    who_notified = 'direction'
            elif self.employee_id.type_employee == 'department_chief' :
                if self.direction_id:
                    who_notified = 'direction'
            else :
                pass
            self.state = 'wait'


    def action_validate(self):
        for rec in self:
            rec.state = 'done'
            #TODO :  notifier le demandeur


    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    def action_reject(self):
        for rec in self:
            rec.state = 'reject'


    def action_to_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.constrains
    def _check_contraints(self):
        if self.date_from > self.date_end:
            raise ValidationError("La date de fin doit être touujours supérieure à la date de début")
        if self.number_of_days_allocate < self.number_of_days:
            raise ValidationError("Impossible d'énregistrer cette opération car le nombre de jours demandés doit "
                                  "être inférieur ou égal au nombre de jous alloués")
