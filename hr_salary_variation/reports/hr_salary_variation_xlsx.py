# -*- coding:utf-8 -*-

import datetime
from odoo import models, api, _

import logging

_logger = logging.getLogger(__name__)

class HrSalaryVariation(models.AbstractModel):
    _name = 'report.hr_salary_variation.report_hr_salary_variation'
    _description = "hr salary variation xlsx"
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

    amount_format= {
        'bold': 1,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '### ### ##0'
    }

    def formatSheet(self, sheet):
        sheet.set_column('A:B', 5)
        sheet.set_column('C:C', 40)

    def generateHeaders(self, sheet, headers, header_format):
        i = 0
        sheet.set_row(i, 30)
        sheet.merge_range(i, 0, i+1, 0, 'N°', header_format)
        sheet.merge_range(i, 1, i+1, 1, 'Matricule', header_format)
        sheet.merge_range(i, 2, i+1, 2, 'NOM ET PRENOMS', header_format)
        idx1 = 3
        idx2 = 6
        for key in headers.keys():
            sheet.merge_range(i, idx1, i, idx2, headers[key], header_format)
            idx1 = idx2+1
            idx2 += 4
        i += 1
        col = 3
        for key in headers.keys():
            sheet.write(i, col, 'Ancien', header_format)
            sheet.write(i, col+1, 'Nouveau', header_format)
            sheet.write(i, col + 2, 'Ecart', header_format)
            sheet.write(i, col+3, 'Observation', header_format)
            col += 4
        i += 1

    def generateLines(self, sheet, elements, codes,c_format):
        i = 2
        for elt in elements:
            col = 1
            _logger.warning(elt)
            if 'matricule' in elt and 'name' in elt and 'line' in elt and 'old_line' in elt:
                sheet.write(i, col, elt['matricule'], c_format)
                sheet.write(i, col+1, elt['name'], c_format)
                col += 2
                line = elt['line']
                old_line = elt['old_line']
                for key in codes.keys():
                    sheet.write(i, col, old_line[key], c_format)
                    col += 1
                    sheet.write(i, col, line[key], c_format)
                    col += 1
                    ecart = line[key] - old_line[key]
                    sheet.write(i, col, ecart, c_format)
                    col += 1
                    sheet.write(i, col, '', c_format)
                    col += 1
                i += 1

    def generateSummary(self, sheet, obj,codes, elements, a_format):
        i = len(elements) + 2

        old_brut = obj.getTotalAmountByCode('BRUT', obj.old_date_from, obj.old_date_to)
        _logger.warning(old_brut)
        brut = obj.getTotalAmountByCode('BRUT', obj.date_from, obj.date_to)
        _logger.warning(brut)
        ecart_brut = brut - old_brut

        old_net = obj.getTotalAmountByCode('NET', obj.old_date_from, obj.old_date_to)
        net = obj.getTotalAmountByCode('NET', obj.date_from, obj.date_to)
        ecart_net = net - old_net

        sheet.merge_range(i, 0, i, 3, 'TOTAL BRUT PÉRIODE PRÉCEDENTE', a_format)
        sheet.merge_range(i, 4, i, 5, old_brut, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 3, 'TOTAL BRUT', a_format)
        sheet.merge_range(i, 4, i, 5, brut, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 3, 'ECART BRUT', a_format)
        sheet.merge_range(i, 4, i, 5, ecart_brut, a_format)
        i += 3

        sheet.merge_range(i, 0, i, 3, 'TOTAL NET PÉRIODE PRÉCEDENTE', a_format)
        sheet.merge_range(i, 4, i, 5, old_net, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 3, 'TOTAL NET', a_format)
        sheet.merge_range(i, 4, i, 5, net, a_format)
        i += 1
        sheet.merge_range(i, 0, i, 3, 'ECART NET', a_format)
        sheet.merge_range(i, 4, i, 5, ecart_net, a_format)
        i += 3

    def generate_xlsx_report(self, workbook, data, obj):
        codes = obj.getCodes()
        obj.getOldPeriodes()
        old_lines = obj.getpayslipLinesForPeriode(codes, obj.old_date_from, obj.old_date_to)

        new_lines = obj.getpayslipLinesForPeriode(codes, obj.date_from, obj.date_to)
        employee_ids = obj.getEmployeePeriode()

        elements = obj.compute_data(employee_ids, new_lines, old_lines, codes)
        _logger.info(elements)

        sheet = workbook.add_worksheet('LIVRE DE PAIE')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.header_format)
        content_format = workbook.add_format(self._content_format)
        amount_format = workbook.add_format(self.amount_format)
        self.formatSheet(sheet)
        #self.i = 3
        self.generateHeaders(sheet, codes, header_format)
        self.generateLines(sheet, elements, codes, content_format)
        self.generateSummary(sheet, obj, codes, elements, amount_format )
