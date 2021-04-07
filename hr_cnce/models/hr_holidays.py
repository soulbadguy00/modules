# -*- conding:utf-8 -*-

from odoo import api, fields, models, _
from dateutil import relativedelta
from datetime import datetime
from odoo.exceptions import UserError, Warning

class HrHolidays(models.Model):
    _inherit = "hr.leave"


    def send_notification(self, email_id, context=None):
        for rec in self:
            template_id = rec.env['ir.model.data'].get_object_reference('hr_cnce', email_id)
            try:
                mail_templ = rec.env['mail.template'].browse(template_id[1])
                result = mail_templ.send_mail(res_id=rec.id, force_send=True)
                return True
            except:
                return False


    @api.depends('employee_id')
    def action_submit(self):
        for rec in self:
            if rec.employee_id.type_employee in ('employee', 'service_chief'):
                if rec.employee_id.department_id:
                    rec.send_notification('email_departement_template_holidays')
                    rec.state = 'department'
                else:
                    rec.state = 'direction'
                    rec.send_notification('email_director_template_holidays')

            elif rec.employee_id.type_employee == 'department_chief':
                rec.state = 'direction'
                rec.send_notification('email_director_template_holidays')
            else:
                rec.state = 'confirm'
                rec.send_notification('email_manager_template_holidays')
            return True


    def action_chief_service(self):
        for rec in self:
            rec.state = 'department'


    def action_chief_department(self):
        for rec in self:
            print("Ok cool")
            rec.state = 'direction'


    def action_chief_direction(self):
        for rec in self:
            rec.state = 'drh'


    @api.depends('company_id')
    def _compute_notif_holidays(self):
        for rec in self:
            if rec.company_id:
                # date_start = str(fields.Date.from_string(rec.date_from) + relativedelta.relativedelta(
                #     days=- rec.company_id.days_before_holidays))
                print('L66',rec.date_from)
                print('L67', rec.company_id.days_before_holidays)
                if rec.date_from and rec.company_id.days_before_holidays:
                    date_start = str(fields.Date.from_string(rec.date_from) + relativedelta.relativedelta(
                         days=- rec.company_id.days_before_holidays))
                    rec.date_noty_start = date_start
                    print('L70', date_start)
                if rec.date_to and rec.company_id.days_after_holidays:
                    date_to = str(fields.Date.from_string(rec.date_to) + relativedelta.relativedelta(
                        days=- rec.company_id.days_after_holidays))
                    rec.date_noty_return = date_to
                    print('L71', date_to)


    def action_confirm(self):
        for rec in self:
            rec.write({'state': 'confirm'})
            rec.activity_update()
            for hol in rec:
                hol.send_notification('email_validation_template_holidays')
            return True


    def _get_link(self):
        for rec in self:
            param_obj = rec.env['ir.config_parameter']
            db = rec._cr.dbname
            board_link = param_obj.get_param('web.base.url')
            board_link += "/?db=%s#id=%s&view_type=form&model=hr.leave" % (db, rec._ids[0])
            print
            board_link
            return board_link

    state = fields.Selection(selection_add=[('direction', 'Directeur'), ('department', 'Chef de departement'),
                                ('service', 'Chef de service')], default="draft")
    direction_id = fields.Many2one('hr.department', 'Direction', required=False, related="employee_id.direction_id")
    service_id = fields.Many2one('hr.department', 'Service', required=True, related="employee_id.service_id")
    motif_refus = fields.Text("Motif de refus", required=False)
    company_id = fields.Many2one('res.company', "Société", default=lambda self: self.env.user.company_id.id)
    date_noty_start = fields.Date("Date de notification de depart", compute="_compute_notif_holidays", store=True)
    date_noty_return = fields.Date("Date de notification de retour", compute="_compute_notif_holidays", store=True)
    justification = fields.Binary('Justification')
    vacation_destination = fields.Selection([('out', 'Hors du pays'), ('in', "À l'intérieur du pays")], 'Destination pendant le congé',
        default=False, states={'validate': [('readonly', True)]})
    interim_id = fields.Many2one('hr.employee', 'Intérimaire', required=False, states={'validate': [('readonly', True)]})
    code = fields.Char("Code", related="holiday_status_id.code")
    other_contact = fields.Char("N°Tel/e-mail pendant le congé", required=False, states={'validate': [('readonly', True)]})

    link = fields.Char("Lien", compute="_get_link")

    def _check_approval_update(self, state):
        """ Check if target state is achievable. """
        current_employee = self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1)
        is_officer = self.env.user.has_group('hr_holidays.group_hr_holidays_user')
        is_manager = self.env.user.has_group('hr_holidays.group_hr_holidays_manager')
        for holiday in self:
            val_type = holiday.holiday_status_id.leave_validation_type
            if state == 'confirm':
                continue

            if state == 'draft':
                # if holiday.employee_id != current_employee and not is_manager:
                #     raise UserError(_('Only a Leave Manager can reset other people leaves.'))
                continue

            if not is_officer:
                continue
                #raise UserError(_('Only a Leave Officer or Manager can approve or refuse leave requests.'))

            if is_officer:
                # use ir.rule based first access check: department, members, ... (see security.xml)
                holiday.check_access_rule('write')

            if holiday.employee_id == current_employee and not is_manager:
                continue
                #raise UserError(_('Only a Leave Manager can approve its own requests.'))

            if (state == 'validate1' and val_type == 'both') or (state == 'validate' and val_type == 'manager'):
                manager = holiday.employee_id.parent_id or holiday.employee_id.department_id.manager_id
                if (manager and manager != current_employee) and not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    raise UserError(_('You must be either %s\'s manager or Leave manager to approve this leave') % (holiday.employee_id.name))

            if state == 'validate' and val_type == 'both':
                if not self.env.user.has_group('hr_holidays.group_hr_holidays_manager'):
                    raise UserError(_('Only an Leave Manager can apply the second approval on leave requests.'))