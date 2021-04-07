# -*- coding:utf-8 -*-

from odoo import api, models, fields, _

class HrHolidaysWizard(models.TransientModel):
    _name = 'hr.holidays.refuse.wizard'
    _description = "hr holidays refuse wizard"

    motif_refus = fields.Text('Motif de refus', required=True)


    def action_refus(self):
        for rec in self:
            holidays = rec.env['hr.leave'].browse(rec.env.context.get('active_id'))
            if holidays:
                holidays.write({
                    'motif_refus': rec.motif_refus
                })
                holidays.action_refuse()