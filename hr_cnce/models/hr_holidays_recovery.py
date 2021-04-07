# -*- coding:utf-8 -*-

from odoo import api, fields, _, models
from dateutil import relativedelta


class HrHolidaysRecovery(models.Model):
    _name = "hr.holidays.recovery"
    _description = "HR Holidays Recovery"
    _rec_name = "employee_id"

    employee_id = fields.Many2one('hr.employee', 'Employé', required=True)
    holidays_id = fields.Many2one('hr.leave', 'Congé', required=True, domain="[('employee_id', '=', employee_id),"
                                     "('state', '=', 'validate')]")
    recovery_date = fields.Date("Date de reprise", required=True)
    recovery_hour = fields.Char("Heure de réprise", required=True)
    number_of_holidays = fields.Float("Nombre de jours", required=True, readonly=True, related="holidays_id.number_of_days")
    direction_id = fields.Many2one("hr.department", "Direction", related="employee_id.direction_id")
    department_id = fields.Many2one("hr.department", "Departement", related="employee_id.department_id")
    service_id = fields.Many2one("hr.department", "Service", related="employee_id.service_id")
    state = fields.Selection([('draft', "brouillon"), ("service", "Chef de service"),
                          ("department", "Chef de departement"), ('direction', "Directeur"), ('drh', "Driecteur des RH"),
                          ('done', "Validé"), ('cancel', "Annulé")], "Etat", default="draft")
    validator_id = fields.Many2one('hr.employee', 'Validateur', required=False, related='employee_id.parent_id')

    @api.onchange('holidays_id')
    def onChangeHoliday(self):
        self.recovery_date = self.holidays_id.request_date_to


    # @api.multi
    # def action_submit(self):
    #     for data in self:
    #         data.state = 'service'


    @api.depends('employee_id')
    def action_submit(self):
        for rec in self:
            if rec.employee_id.type_employee in ('employee', 'service_chief'):
                if rec.employee_id.department_id:
                    #self.send_notification('email_departement_template_holidays')
                    rec.state = 'department'
                else:
                    rec.state = 'direction'
                    #self.send_notification('email_director_template_holidays')

            elif rec.employee_id.type_employee == 'department_chief':
                rec.state = 'direction'
                #self.send_notification('email_director_template_holidays')
            else:
                rec.state = 'confirm'
                #self.send_notification('email_manager_template_holidays')
            return True


    def action_chief_service(self):
        for data in self:
            data.state = 'department'


    def action_chief_departement(self):
        for data in self:
            data.state = 'direction'


    def action_chief_direction(self):
        for data in self:
            data.state = 'drh'


    def action_done(self):
        for data in self:
            data.state = 'done'


    def action_cancel(self):
        for data in self:
            data.state = 'cancel'


    def action_to_draft(self):
        for data in self:
            data.state = 'draft'