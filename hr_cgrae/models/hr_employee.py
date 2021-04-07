# -*- coding:utf-8 -*-


from odoo import api, models, fields, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    type = fields.Selection(selection_add=[('p', 'Fonctionnaire')])


class CategorieSalariale(models.Model):
    _inherit = "hr.categorie.salariale"

    brut_indiciaire = fields.Integer("Brut Indiciaire")