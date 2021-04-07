# -*- coding:utf-8 -*-

from odoo import api, models, fields, _


class hrsalaryRule(models.Model):
    _inherit = "hr.salary.rule"

    is_tax_fdfp = fields.Boolean("Est un impôt FDFP")