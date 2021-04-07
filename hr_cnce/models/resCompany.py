# -*- coding:utf-8 -*-

from odoo import api, fields, models, _

class ResCompany(models.Model):
    _inherit = 'res.company'

    direction_general_note = fields.Text("Mot de la direction général", required=False)
    hr_manager_id = fields.Many2one('hr.employee', 'Directeur des Ressources Humaines', required=True)
    days_before_holidays = fields.Integer(string="Alerte avant congés (Jours)")
    days_after_holidays = fields.Integer(string="Alerte après congés (Jours)")
    first_alert_retraite = fields.Integer(string="Première alerte depart retraite (Mois)", readonly=False)
    second_alert_retraite = fields.Integer(string="Deuxième alerte depart retraite (Mois)", readonly=False)
    signature_drh = fields.Binary("Singature du DRH", required=False)
