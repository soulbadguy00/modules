# -*- coding:utf-8 -*-


from odoo import api, models, fields, _
from num2words import num2words


class ProductTemplate(models.Model):
    _inherit = "product.template"

    temperature = fields.Float("température de stockage en °C")