# -*- coding: utf-8 -*-
# Copyright 2019 Demodoo IT Solutions
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _


class Groups(models.Model):

    _inherit = 'res.groups'

    ext_id = fields.Char('External Id', default='', compute='_compute_ext_id', search='_search_ext_id',
                         help="External Id of the access group.")

    def _compute_ext_id(self):
        for record in self:
            group_obj_l = self.env['ir.model.data'].sudo().search([('res_id', '=', record.id),
                                                                   ('model', '=', 'res.groups')], limit=1)
            if group_obj_l:
                group_obj = group_obj_l[0]
                record.ext_id = '%s.%s' % (group_obj.module, group_obj.name)
            else:
                record.ext_id = ''

    def _search_ext_id(self, operator, value):
        domain = [('model', '=', 'res.groups'), '|', ('name', operator, value), ('module', operator, value)]
        data = self.env['ir.model.data'].sudo().search(domain)
        return [('id', 'in', data.mapped('res_id'))]
