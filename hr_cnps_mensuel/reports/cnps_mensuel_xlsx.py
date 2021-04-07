# -*- coding:utf-8 -*-

import datetime


from odoo import models




class HrPayrollPayrollWizardXlsx(models.AbstractModel):

    _name = 'report.hr_cnps_mensuel.cnps_mensuel_report_xlsx'
    _description = "cnps mensuel rapport xlsx"
    _inherit = 'report.report_xlsx.abstract'

    #i = 0

    title = ['NUMERO CNPS', 'NOM ET PRENOMS', 'ANNEE DE NAISSANCE', "DATE D'EMBAUCHE", "DATE DE DEPART", 'TYPE SALARIE M: Mensuel J : Journalier '
              'H: Horaire', 'DUREE TRAVAILLEE', 'SALAIRE BRUT']

    # Formattage pour les headers
    h_format = {
        'bold': 1,
        'border': 1,
        'font_size': 10,
        'align': 'center',
        'valign': 'vcenter',
        'fg_color': 'gray',
        'text_wrap': 1
    }

    c_format = {
        'bold': 0,
        'border': 1,
        'align': 'left',
        'valign': 'vcenter',
        'fg_color': 'white'
    }

    a_format = {
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '### ### ##0'
    }

    a_total_format = {
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '### ### ##0',
        'fg_color': 'gray',
    }

    def formatSheet(self, sheet):
        sheet.set_column('A:A', 40)
        sheet.set_column('B:ZZ', 15)

    def generateLines(self, sheet, obj, c_format):
        row = 1
        for line in obj.other_line_ids:
            sheet.write(row, 0, line.employee_id.matricule_cnps, c_format)
            sheet.write(row, 1, line.employee_id.name, c_format)
            sheet.write(row, 2, str(line.employee_id.birthday.year), c_format)
            sheet.write(row, 3, str(line.employee_id.start_date), c_format)
            sheet.write(row, 4, str(line.employee_id.end_date), c_format)
            sheet.write(row, 5, line.employee_id.type, c_format)
            sheet.write(row, 6, 1, c_format)
            sheet.write(row, 7, line.amount_brut, c_format)
            row += 1

    def writeHeaders(self, sheet, obj,h_format):
        col = 0
        line = 0
        for i in range(len(self.title)):
            sheet.write(line, col, self.title[i], h_format)
            col += 1
        #self.line += 1

    #def generate_xlsx_report(self, workbook, data, partners):
    def generate_xlsx_report(self, workbook, data, obj):

        sheet = workbook.add_worksheet('LIVRE DE PAIE')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.h_format)
        content_format = workbook.add_format(self.c_format)
        amount_format = workbook.add_format(self.a_format)
        amount_total_format = workbook.add_format(self.a_total_format)
        self.formatSheet(sheet)
        #self.line = 0
        self.writeHeaders(sheet, obj, header_format)
        self.generateLines(sheet, obj, content_format)
