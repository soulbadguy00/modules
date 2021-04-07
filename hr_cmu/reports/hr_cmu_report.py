# -*- coding:utf-8 -*-

import datetime
from odoo import models, fields, api, _


class HrCMURapportXlsx(models.AbstractModel):
    _name = 'report.hr_cmu.cmu_rapport_xlsx'
    _description = "CMU rapport xlsx"
    _inherit = 'report.report_xlsx.abstract'

    #i = fields.Integer('compteur', default=0)
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
        "NUMERO CNPS \nBENEFICIAIRE",
        "NUMERO \nSECURITE SOCIALE \nBENEFICIAIRE",
        "TYPE BENEFICIAIRE \nC: CONJOINT \nT: TRAVAILLEUR \nE: ENFANT",
        "NOM BENEFICIAIRE",
        "PRENOMS BENEFICIAIRE",
        "GENRE \nBENEFICIAIRE \nH: HOMME \nF: FEMME"
    )

    # i = 0

    def formatSheet(self, sheet):
        sheet.set_column('A:A', 40)
        sheet.set_column('B:V', 15)

    def generateHeaders(self, sheet, header_format):
        col = 0

        sheet.set_row(0, 30)
        for x in range(len(self.headers)):
            sheet.write(0, col, self.headers[x], header_format)
            col += 1
        #self.i += 1

    def generateLines(self, sheet, lines, content_format):
        cpt = 1
        for line in lines:
            #self.i = self.i + 1
            sexe = "M"
            sheet.write(cpt, 0, line.num_cnps, content_format)
            sheet.write(cpt, 1, line.num_cmu, content_format)
            sheet.write(cpt, 2, str(line.type).upper(), content_format)
            sheet.write(cpt, 3, line.name, content_format)
            sheet.write(cpt, 4, line.first_name, content_format)
            if line.gender == 'female':
                sexe = "F"
            elif line.gender == 'male':
                sexe = "H"
            else:
                sexe = ''
            sheet.write(cpt, 5, sexe, content_format)
            cpt += 1

    def generateLinesTotaux(self, sheet, totaux, codes, amount_format, content_format):
        col = 0
        sheet.write(self.i, col, 'TOTAUX', content_format)
        for code in codes:
            col += 1
            sheet.write(self.i, col, totaux[code], amount_format)

    def generate_xlsx_report(self, workbook, data, obj):
        sheet = workbook.add_worksheet('Rapport CMU')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.header_format)
        content_format = workbook.add_format(self.content_format)
        amount_format = workbook.add_format(self.amount_format)
        self.formatSheet(sheet)
        # self.i = 0
        self.generateHeaders(sheet, header_format)
        if obj.line_ids:
            self.generateLines(sheet, obj.line_ids, content_format)
            #self.generateLinesTotaux(sheet, totaux, results['codes'], amount_format, content_format,obj.line_ids)
