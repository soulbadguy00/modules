# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import time

from odoo import api, fields, models, _
from odoo.exceptions import UserError


# class HolidaysSummaryDept(models.TransientModel):
#
#     _inherit = 'hr.holidays.summary.dept'
#
#     depts = fields.Many2many('hr.department', 'summary_dept_rel', 'sum_id', 'dept_id', string='Department(s)')
#     holiday_type = fields.Selection([
#         ('Approved', 'Approved'),
#         ('Confirmed', 'Confirmed'),
#         ('both', 'Both Approved and Confirmed')
#     ], string='Status', required=True, default='Approved')
#     type = fields.Many2one('hr.leave.type', "Type")
#     date_to = fields.Date(string='À', required=True)