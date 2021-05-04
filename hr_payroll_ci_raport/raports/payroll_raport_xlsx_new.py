# -*- coding:utf-8 -*-

from odoo import models


# ----------------------------------------------------------
# Payroll xlsx or xls (excel) new format
# ----------------------------------------------------------
class HrPayrollPayrollXlsxNew(models.AbstractModel):
    _name = 'report.hr_payroll_ci_raport.hr_payroll_xlsx_new'
    _description = " rapport hr payroll xlsx new"
    _inherit = 'report.report_xlsx.abstract'

    # Formatting for header
    header_format = {
        'bold': 0,
        'border': 0,
        'align': 'right',
        'valign': 'vcenter',
        'fg_color': '#a6a6a6',
        'text_wrap': 0,
        'font_name': 'Calibri',
        'font_size': 11,
        'num_format': '# ##0',
    }

    # Formatting for content
    content_format = {
        'bold': 0,
        'border': 0,
        'align': 'left',
        'valign': 'vcenter',
        'font_name': 'Calibri',
        'font_size': 11
    }

    # Formatting for amount
    amount_format = {
        'bold': 0,
        'border': 0,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '# ##0',
        'font_name': 'Calibri',
        'font_size': 11
    }

    def formatSheet(self, sheet):
        """
        Format sheet
        :param sheet:
        :return:
        """
        sheet.set_column('A:A', 20)  # set_column(first_col, last_col, width, cell_format, options)
        sheet.set_column('B:B', 30)  # set_column(first_col, last_col, width, cell_format, options)
        sheet.set_column('C:W', 20)  # set_column(first_col, last_col, width, cell_format, options)

    def generateHeaders(self, sheet, headers, header_format):
        """
        Generate header sheet
        :param sheet:
        :param headers:
        :param header_format:
        :return:
        """
        col = 0
        sheet.set_row(0, 30)
        for code in headers:
            sheet.write(0, col, code, header_format)  # (row, col, data, format)
            col += 1

    def generateLines(self, workbook, sheet, lines, rules, amount_format, content_format):
        """
        Generate lines sheet
        :param sheet:
        :param lines:
        :param codes:
        :param amount_format:
        :param content_format:
        :return:
        """
        row = 0
        col = 2
        cell_format_total = workbook.add_format({'fg_color': '#a6a6a6'})
        count = len(lines)
        if count > 0:
            page = count / 4  # 5 employee by page
            print('page', page)
        for line in lines:
            i = 5
            sheet.write(row, 0, 'N matricule', content_format)  # (row, col, data, format)
            sheet.write(row + 1, 0, 'Section analytique', content_format)  # (row, col, data, format)
            sheet.write(row + 2, 0, 'Catégorie', content_format)  # (row, col, data, format)
            sheet.write(row + 3, 0, 'Nom', content_format)  # (row, col, data, format)
            sheet.write(row + 4, 0, 'Prénoms', content_format)  # (row, col, data, format)

            sheet.write(row, 1, "", content_format)  # (row, col, data, format)
            sheet.write(row + 1, 1, "", content_format)  # (row, col, data, format)
            sheet.write(row + 2, 1, "", content_format)  # (row, col, data, format)
            sheet.write(row + 3, 1, "", content_format)  # (row, col, data, format)
            sheet.write(row + 4, 1, "", content_format)  # (row, col, data, format)

            sheet.write(row, col, line['identification'], content_format)  # (row, col, data, format)
            sheet.write(row + 1, col, line['analytic_section'], content_format)  # (row, col, data, format)
            sheet.write(row + 2, col, line['category'], content_format)  # (row, col, data, format)
            sheet.write(row + 3, col, line['lastname'], content_format)  # (row, col, data, format)
            sheet.write(row + 4, col, line['firstname'], content_format)  # (row, col, data, format)
            for rule in rules:
                if 299 > rule.sequence >= 100:
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                if rule.sequence == 300:  # Brut imposable
                    # sheet.set_row(i, 6, cell_format_total)
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                if 449 >= rule.sequence >= 400:  # retenues salariales
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                if rule.sequence == 499:  # total retenue salariale
                    # sheet.set_row(i, 6, cell_format_total)
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                if 498 >= rule.sequence > 449:  # retenues patronales
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                # mettre ici total retenues patronales
                if 599 > rule.sequence >= 501:  # autres retenues
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                # mettre ici total autres retenues
                if 799 >= rule.sequence >= 700:  # autres retenues
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)
                if rule.sequence == 800:
                    # sheet.set_row(i, 6, cell_format_total)
                    sheet.write(i, 0, rule.sequence, amount_format)
                    sheet.write(i, 1, rule.name, content_format)
                    sheet.write(i, col, line[rule.code], amount_format)

                i += 1

            col += 1

    def generateLinesTotaux(self, sheet, totaux, codes, amount_format, content_format, lines):
        """
        Generate totals sheet
        :param sheet:
        :param totaux:
        :param codes:
        :param amount_format:
        :param content_format:
        :param lines:
        :return:
        """
        i = len(lines) + 1
        col = 0
        sheet.write(i, col, 'TOTAUX', content_format)
        for code in codes:
            col += 1
            sheet.write(i, col, totaux[code], amount_format)  # (row, col, data, format)

    def generate_xlsx_report(self, workbook, data, lines):
        """
        Generate report to excel (xls, xlsx)
        :param workbook:
        :param data:
        :param lines:
        :return:
        """
        report_payroll_obj = self.env['report.hr_payroll_ci_raport.report_payroll']
        results = report_payroll_obj._lines_new(data['form']['date_from'], data['form']['date_to'],
                                                data['form']['company_id'],
                                                data['form']['type_employe'])
        # totaux = report_payroll_obj._lines_total(results['codes'], results['lines'])

        sheet = workbook.add_worksheet(data['form']['name'])  # Defaults to Sheet1.
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.header_format)
        content_format = workbook.add_format(self.content_format)
        amount_format = workbook.add_format(self.amount_format)
        title = data['form']['name']
        sheet.write(0, 0, title, bold)  # (row, col, data, format)
        self.formatSheet(sheet)
        # self.generateHeaders(sheet, results['headers'], header_format)
        self.generateLines(workbook, sheet, results['lines'], results['rules'], amount_format, content_format)
        # self.generateLinesTotaux(sheet, totaux, results['codes'], amount_format, content_format, results['lines'])
        # sheet.fit_to_pages(2, 1)  # Fit to 2x1 pages.
