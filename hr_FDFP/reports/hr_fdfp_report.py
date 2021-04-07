# -*- coding: utf-8 -*-

import time
from odoo import api, models


class ReportHrPayroll(models.AbstractModel):
    _name = 'report.hr_payroll_ci_raport.report_hr_fdfp'

    @api.model
    def get_report_values(self, docids, data=None):
        self.model = data['model']
        docs = self.env[self.model].browse(data['ids'])
        print(data)
        lang_code = self.env.context.get('lang') or 'fr_FR'
        lang = self.env['res.lang']
        lang_id = lang._lang_get(lang_code)
        date_format = lang_id.date_format

        return {
            'doc_ids': self.ids,
            'doc_model': self.model,
            'data': data,
            'docs': docs,
            'time': time,
        }

