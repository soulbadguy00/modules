# -*- coding:utf-8 -*-

import datetime
from odoo import models, api, _


class HrCRRAEapportXlsx(models.AbstractModel):
    _name = "report.hr_crrae.hr_crrae_raport.xlsx"
    _description = "hr crrae rapport xlsx"
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

    content_format = {
        'bold': 0,
        'border': 1,
        'align': 'left',
        'valign': 'vcenter',
        'fg_color': 'white'
    }

    amount_format = {
        'bold': 1,
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '# ##0'
    }

    headers = (
        "REGIME DE RETRAITE(O)",
        "MATRICULE ENTREPRISE(O)",
        "MATRICULE CRRAE(O)",
        "NOM(O)",
        "PRENOMS(O)",
        "TYPE COTISATION(O)",
        "PERIODE DE COTISATION",
        "PERIODE A REGULARISER (F)",
        "ASSIETTE",
        "MOTIF CHANGEMENT ASSIETTE(F)",
        "PART EMPLOYE(O)",
        "PART EMPLOYEUR(O)",
        "TOTAL COTISATION(O)",
        "TOTAL(O)",
        "ETAT PARTICIPANT(F)",
        "DATE DE CHANGEMENT D'ÉTAT(F)",
        "PART EMPLOYÉ FAAM",
        "PART EMPLOYEUR FAAM",
        "TOTAL COTISATION FAAM"
    )

    def formatSheet(self, sheet):
        sheet.set_column('A:A', 40)
        sheet.set_column('B:V', 15)

    def generateHeaders(self, sheet, header_format):
        col = 0
        line = 0
        sheet.set_row(0, 30)
        for x in range(len(self.headers)):
            sheet.write(line, col, self.headers[x], header_format)
            col += 1
        #line += 1

    def generateLine(self, sheet, obj, dt, content_format,line):
        line = line
        if dt['crrae_employer']:
            sheet.write(line, 0, 'RRPC', content_format)
            sheet.write(line, 1, dt['matricule'], content_format)
            sheet.write(line, 2, dt['num_crrae'], content_format)
            sheet.write(line, 3, dt['name'], content_format)
            sheet.write(line, 4, dt['prenoms'], content_format)
            sheet.write(line, 5, "NOR", content_format)
            sheet.write(line, 6, obj.periode, content_format)
            sheet.write(line, 7, obj.periode_regul, content_format)
            sheet.write(line, 8, obj.assiette, content_format)
            sheet.write(line, 9, obj.motif_changement, content_format)
            sheet.write(line, 10, dt['crrae_employee'], content_format)
            sheet.write(line, 11, dt['crrae_employer'], content_format)
            # sheet.write(line, 12, dt['crrae_employee'] + dt['crrae_employer'], content_format)
            # sheet.write(line, 13, dt['crrae_employee'] + dt['crrae_employer'], content_format)
            sheet.write(line, 12, 100 + dt['crrae_employer'], content_format)
            sheet.write(line, 13, 100 + dt['crrae_employer'], content_format)

            sheet.write(line, 16, dt['faam_employee'], content_format)
            sheet.write(line, 17, dt['faam_employer'], content_format)
            #sheet.write(line, 18, dt['faam_employee'] + dt['faam_employer'], content_format)
            sheet.write(line, 18, dt['faam_employer'], content_format)

            # sheet.write(self.i, 6, line.gender, content_format)
            #self.i += 1

    def generateLinesTotaux(self, sheet, totaux, codes, amount_format, content_format):
        col = 0
        line = 100
        sheet.write(line, col, 'TOTAUX', content_format)
        for code in codes:
            col += 1
            sheet.write(line, col, totaux[code], amount_format)
        line += 1

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('CMU')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.header_format)
        content_format = workbook.add_format(self.content_format)
        amount_format = workbook.add_format(self.amount_format)
        self.formatSheet(sheet)
        #self.i = 0
        self.generateHeaders(sheet, header_format)
        datas = self._context.get('data')
        if datas:
            line = 2
            for dt in datas:
                self.generateLine(sheet, obj, dt, content_format,line)
                line += 1
