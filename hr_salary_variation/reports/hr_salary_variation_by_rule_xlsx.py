# -*- coding:utf-8 -*-

import datetime
from odoo import models, api, _

class HrSalaryVariationByRule(models.AbstractModel):
    _name = 'report.hr_salary_variation.report_hr_salary_variation_by_rule'
    _description = "hr salary variation report "
    _inherit = 'report.report_xlsx.abstract'

    #i = 0

    # Formattage pour les headers
    header_format = {
        'bold': 1,
        'border': 1,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'gray',
        'text_wrap': 1
    }

    _content_format = {
        'bold': 0,
        'border': 1,
        'align': 'left',
        'valign': 'vcenter',
        'fg_color': 'white'
    }

    _amount_format = {
        'bold': 1,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '### ### ##0'
    }

    def formatSheet(self, sheet):
        sheet.set_column('A:A', 10)
        sheet.set_column('B:B', 30)
        sheet.set_column('C:E', 15)
        sheet.set_column('F:F', 50)

    def generateHeaders(self, sheet, header_format):
        i = 0
        sheet.set_row(i, 30)
        sheet.write(i, 0, 'RUBRIQUE', header_format)
        sheet.write(i, 1, 'LIBELLÉ RUBRIQUE', header_format)
        sheet.write(i, 2, 'MOIS PRÉCÉDENT', header_format)
        sheet.write(i, 3, 'MOIS EN COURS', header_format)
        sheet.write(i, 4, 'ECART', header_format)
        sheet.write(i, 5, 'OBSERVATION', header_format)
        #i += 1

    def generateLines(self, sheet, elements, c_format):
        i = 1
        for elt in elements:
            col = 0
            sheet.write(i, col, elt['code'], c_format)
            sheet.write(i, col+1, elt['name'], c_format)
            sheet.write(i, col + 2, elt['old_amount'], c_format)
            sheet.write(i, col + 3, elt['new_amount'], c_format)
            sheet.write(i, col + 4, elt['ecart'], c_format)
            sheet.write(i, col + 5, '', c_format)
            i += 1

    def generateSummary(self, sheet, obj, elements, a_format):
        i = len(elements) + 2

        old_brut = obj.getTotalAmountByCode('BRUT', obj.old_date_from, obj.old_date_to)
        brut = obj.getTotalAmountByCode('BRUT', obj.date_from, obj.date_to)
        ecart_brut = brut - old_brut

        old_net = obj.getTotalAmountByCode('NET', obj.old_date_from, obj.old_date_to)
        net = obj.getTotalAmountByCode('NET', obj.date_from, obj.date_to)
        ecart_net = net - old_net
        print('L78')
        sheet.merge_range(i, 0, i, 2, 'TOTAL BRUT PÉRIODE PRÉCEDENTE', a_format)
        sheet.merge_range(i, 3, i, 4, old_brut, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 2, 'TOTAL BRUT', a_format)
        sheet.merge_range(i, 3, i, 4, brut, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 2, 'ECART BRUT', a_format)
        sheet.merge_range(i, 3, i, 4, ecart_brut, a_format)
        i += 3

        sheet.merge_range(i, 0, i, 2, 'TOTAL NET PÉRIODE PRÉCEDENTE', a_format)
        sheet.merge_range(i, 3, i, 4, old_net, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 2, 'TOTAL NET', a_format)
        sheet.merge_range(i, 3, i, 4, net, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 2, 'ECART NET', a_format)
        sheet.merge_range(i, 3, i, 4, ecart_net, a_format)
        #i += 3
        print('L98')

    def generate_xlsx_report(self, workbook, data, obj):
        codes = obj.getCodes()
        obj.getOldPeriodes()
        old_lines = obj.getpayslipLinesForPeriode(codes, obj.old_date_from, obj.old_date_to)

        new_lines = obj.getpayslipLinesForPeriode(codes, obj.date_from, obj.date_to)

        results = obj.getVariationByRule(codes)

        sheet = workbook.add_worksheet('LIVRE DE PAIE')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.header_format)
        content_format = workbook.add_format(self._content_format)
        amount_format = workbook.add_format(self._amount_format)
        self.formatSheet(sheet)
        #self.i = 3
        print('L115')
        self.generateHeaders(sheet, header_format)
        print('L117')
        self.generateLines(sheet, results, content_format)
        print('L119')
        self.generateSummary(sheet, obj, results, amount_format)
        print('L121')