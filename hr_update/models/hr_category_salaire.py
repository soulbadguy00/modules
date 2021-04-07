# -*- coding:utf-8 -*-

from odoo import fields, api, models, _, exceptions


class HrCategorieSalaire(models.Model):
    _name = "hr.categorie.salaire"
    _description = "hr categorie salaire"

    name = fields.Char('Libellé', required=True)
    sequence = fields.Integer('Séquence', required=True, default=10)
    active = fields.Boolean('Actif')
    code = fields.Char('Code', size=2, required=True)
    description = fields.Text('Description')
