# -*- conding:utf-8 -*-

from odoo import api, fields, models, _

from dateutil import relativedelta


class HrCatgeryContract(models.Model):
    _name = "hr.category.contract"
    _description = "hr category contract"

    name = fields.Char("Libelle ", required=True)
    delai_notif_fin = fields.Integer("Notifier à combien de jours de fin contrat", required=True)
    delai_notif_essai = fields.Integer("Notifier à combien de jours de la période d'essai", required=False)
    description = fields.Text("Description", required=False)


class HrContractNoitificationLine(models.Model):
    _name = "hr.contract.notification.line"
    _description = "hr contract notification line"

    date_notification = fields.Date("Date de notification", required=True)
    contract_id = fields.Many2one('hr.contract', 'Contrat', required=False)


class HrContract(models.Model):
    _inherit = "hr.contract"

    notification_lines_ids = fields.One2many('hr.contract.notification.line', 'contract_id',
                                             "Les dates de notification")
    category_contract_id = fields.Many2one('hr.category.contract', 'Catégorie de contrat', required=False,
                                           help="Utiliser STAGE pour définir les stages")
    date_noty_fin_contract = fields.Date("Date de notification de fin")
    date_noty_fin_essai = fields.Date('Date de nofitication de fin essai')
    notify_model_id = fields.Many2one(required=False)

    def send_notification(self, email_id, context=None):
        for rec in self:
            template_id = rec.ev['ir.model.data'].get_object_reference('hr_cnce', email_id)
            try:
                mail_templ = rec.env['mail.template'].browse(template_id[1])
                result = mail_templ.send_mail(res_id=rec.id, force_send=True)
                return True
            except:
                return False

    @api.onchange('date_end', 'trial_date_end', 'category_contract_id')
    @api.depends('date_end', 'trial_date_end', 'category_contract_id')
    def compute_date_noty(self):
        if self.category_contract_id:
            if self.date_end:
                date_temp = fields.Date.from_string(self.date_end)
                this_date = str(
                    date_temp + relativedelta.relativedelta(days=- self.category_contract_id.delai_notif_fin))
                self.date_noty_fin_contract = this_date
            if self.trial_date_end:
                date_temp = fields.Date.from_string(self.trial_date_end)
                this_date = str(
                    date_temp + relativedelta.relativedelta(days=- self.category_contract_id.delai_notif_essai))
                self.date_noty_fin_essai = this_date

    @api.onchange('notify_model_id', 'date')
    def compute_notification(self):
        self.notification_lines_ids = []
        if self.notify_model_id:
            if self.date_end:
                date = fields.Datetime.from_string(self.date_end)
                data = self.notify_model_id.getNotifLine(date)
                self.notification_lines_ids = data
