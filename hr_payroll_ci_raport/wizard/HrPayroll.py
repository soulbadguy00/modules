# -*- coding:utf-8 -*-
__author__ = 'ropi'

from odoo import fields, models, api, _, tools
from odoo.exceptions import UserError

import babel
from datetime import date, datetime, time
# import xlwt
# from xlsxwriter.workbook import Workbook
# import base64
# from dateutil.relativedelta import relativedelta
# from pytz import timezone


class HrPayroll(models.TransientModel):
    _name = 'hr.payroll.payroll'
    _description = "Gestion des livres de paie"

    @api.onchange('date_from', 'company_id')
    @api.depends('date_from', 'company_id')
    def onchange_company(self):
        self.name = self.company_id.name
        locale = self.env.context.get('lang') or 'en_US'
        if self.date_from:
            ttyme = datetime.combine(self.date_from, time.min)
            name = 'Livre de paie %s de %s' % (self.company_id.name, tools.ustr(babel.dates.format_date(date=ttyme,
                                                                                                        format='MMMM-y',
                                                                                                        locale=locale)))
            self.name = str(name).upper()

    name = fields.Char('Libellé', required=True, size=155)
    # lot_id = fields.Many2one('h.payslip.run', 'Lot de paie', required=True)
    date_from = fields.Date('Date de début', required=True)
    date_to = fields.Date('Date de fin', required=True)
    company_id = fields.Many2one('res.company', 'Compagnie', required=True, ondelete='cascade', default=1)
    type_employe = fields.Selection([('mensuel', 'Mensuel'),
                                     ('journalier', 'Journalier'),
                                     ('horaire', 'Horaire'), ('all', 'Tous les employés')], "Livre de paie pour:",
                                    default="all")

    def _print_report(self, data):
        # data['form'].update(self.read(['initial_balance', 'sortby'])[0])
        if not data['form'].get('date_from'):
            raise UserError(_("You must define a Start Date"))

        records = self.env[data['model']].browse(data.get('ids', []))
        return self.env.ref('hr_payroll_ci_raport.report_hr_payroll').with_context(landscape=True).report_action(self,
                                                                                                                 data=data)

    # return self.env.ref('account.action_report_journal').with_context(landscape=True).report_action(self, data=data)

    def check_report(self):
        for rec in self:
            rec.ensure_one()
            data = {}
            data['ids'] = rec.id
            data['model'] = 'hr.payroll.payroll'
            data['form'] = rec.read(['name', 'date_from', 'date_to', 'company_id', 'type_employe'])[0]
            return rec._print_report(data)

    def export_xls(self):
        for rec in self:
            context = rec._context
            datas = {'ids': context.get('uid', []), 'model': 'hr.payroll.payroll', 'form': rec.read()[0]}
            for field in datas['form'].keys():
                if isinstance(datas['form'][field], tuple):
                    datas['form'][field] = datas['form'][field][0]
            return rec.env.ref('hr_payroll_ci_raport.payroll_report_xlsx').with_context(data=datas).report_action(rec, data=datas, config=False)

    def export_to_excel(self):
        """
        Export payroll to excel
        __author__
        :return:
        """
        for rec in self:
            context = rec._context
            datas = {'ids': context.get('uid', []), 'model': 'hr.payroll.payroll', 'form': rec.read()[0]}
            for field in datas['form'].keys():
                if isinstance(datas['form'][field], tuple):
                    datas['form'][field] = datas['form'][field][0]
            return rec.env.ref('hr_payroll_ci_raport.payroll_report_xlsx_new').with_context(data=datas).report_action(rec,
                                                                                                                  data=datas,
                                                                                                                  config=False)

    # def export_xls(self):
    #     print('L72 - nouveau rapport')
    #     for rec in self:
    #         data = {}
    #         data['ids'] = rec.id
    #         data['model'] = 'hr.payroll.payroll'
    #         data['form'] = rec.read(['name', 'date_from', 'date_to', 'company_id', 'type_employe'])[0]
    #         print('L78 - data',data)
    #         workbook = xlwt.Workbook(encoding="UTF-8")
    #
    #         header_format = xlwt.easyxf('font: bold True, name Arial')
    #         # format = workbook.add_format({'align': 'left', 'valign': 'top'})
    #         # center_format = workbook.add_format({'align': 'center', 'border': 1, 'num_format': 'mm/dd/yy'})
    #         # bold = workbook.add_format({'align': 'left', 'bold': True})
    #         # center_format_bold = workbook.add_format({'align': 'center', 'bold': True})
    #         # no_format = workbook.add_format({'align': 'center', 'num_format': '#,###', 'border': 1, })
    #         # date_format = workbook.add_format({'num_format': 'dd/mm/yy'})
    #
    #         report_name = data['form']['name'][0]
    #         worksheet = workbook.add_sheet(report_name)
    #
    #         row, col = 1, 0
    #         worksheet.write(row, col, 'N', header_format)
    #         worksheet.write(row, col + 1, "Matricule", header_format)
