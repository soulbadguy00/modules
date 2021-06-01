# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
from odoo.tools.float_utils import float_round
from dateutil.relativedelta import relativedelta


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    temperature = fields.Float('Temperature')


class ProductProduct(models.Model):
    _inherit = 'product.product'

    temperature = fields.Float('Temperature')
