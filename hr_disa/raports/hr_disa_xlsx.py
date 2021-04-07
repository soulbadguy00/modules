# -*- coding:utf-8 -*-

import datetime


from odoo import models




class HrDISA(models.AbstractModel):
    _name = 'report.hr_disa.report_hr_disa'
    _description = "disa rapport xlsx"
    _inherit = 'report.report_xlsx.abstract'

    title = [
        "NUMERO D’ORDRE",
        "NOM & PRENOMS",
        "N° C.N.P.S",
        "ANNEE DE NAISSANCE",
        "DATE D’EMBAUCHE",
        "DATE DE DEPART",
        "TYPE DE SALARIES : HORAIRES (H), JOURNALIERS (J) OU MENSUELS (M)",
        "NOMBRE D’HEURES, DE JOURS OU DE MOIS TRAVAILLES (Y COMPRIS LE CONGE ANNUEL)",
        "SALAIRES BRUTS ANNUELS NON PLAFONNES (Y COMPRIS TOUT AVANTAGE )",
        "SALAIRES ANNUELS SOUMIS A COTISATIONS AU TITRE DE L'ASSURANCE MATERNITE, "
        "DES PRESTATIONS FAMILIALES, DES ACCIDENTS DU TRAVAIL ET MALADIES PROFESSIONNELLES",
        "SALAIRES ANNUELS SOUMIS A COTISATIONS AU TITRE DU REGIME DE LA RETRAITE",
        "L’ENTREPRISE COTISE POUR LE SALARIE AU TITRE DE: 1=PF 2=AT 3=AV 4= AM",
        "Commentaires"
    ]

    cols = [
        'order','employee_name','num_cnps','date_naissance','date_embauche','date_depart','type_employee',
        'temps_travail','brut_total','brut_autre','brut_cnps','cotisation','comment'
    ]

    #i = 0

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
        'num_format': '# ##0'
    }

    a_total_format = {
        'border': 1,
        'align': 'right',
        'valign': 'vcenter',
        'num_format': '# ##0',
        'fg_color': 'gray',
    }

    def formatSheet(self, sheet):
        sheet.set_column('A:A', 5)
        sheet.set_column('B:B', 50)
        sheet.set_column('C:ZZ', 15)


    def generateLines(self, sheet, lines,c_format):
        cpt = 1
        for line in lines:
            col = 0
            for i in range(len(self.cols)):
                key = self.cols[i]
                sheet.write(cpt, col, line[key], c_format)
                col += 1
            cpt += 1

    def writeHeaders(self, sheet, h_format):
        col = 0
        line = 0
        for i in range(len(self.title)):
            sheet.write(line, col, self.title[i], h_format)
            col += 1

    def generate_xlsx_report(self, workbook, data, obj):
        lines = data['lines']
        sheet = workbook.add_worksheet('LIVRE DE PAIE')
        bold = workbook.add_format({'bold': True})
        header_format = workbook.add_format(self.h_format)
        content_format = workbook.add_format(self.c_format)
        amount_format = workbook.add_format(self.a_format)
        amount_total_format = workbook.add_format(self.a_total_format)
        self.formatSheet(sheet)
        self.writeHeaders(sheet,header_format)
        self.generateLines(sheet, lines,content_format)

