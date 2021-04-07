# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from itertools import groupby


class HrITS(models.Model):
    _name = 'hr.its'
    _description = "hr its"

    def _get_effectif_employee(self):
        for rec in self:
            slip_obj = rec.env['hr.payslip']
            all_slips = slip_obj.search([('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to),
                                         ('company_id', '=', rec.company_id.id)])
            if all_slips:
                rec.env.cr.execute("SELECT COUNT (distinct(id)), nature_employe FROM hr_employee WHERE "
                                   "id IN (SELECT employee_id FROM hr_payslip WHERE id=ANY(%s)) "
                                   "GROUP BY nature_employe", (all_slips.ids,))
                result = rec.env.cr.dictfetchall()
                if result:
                    for res in result:
                        if res['nature_employe'] == 'local':
                            rec.total_number_local = res['count']
                        else:
                            rec.total_number_expat = res['count']

    def _get_revenu_employee(self):
        for rec in self:
            slip_obj = rec.env['hr.payslip']
            all_slips = slip_obj.search([('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to),
                                         ('company_id', '=', rec.company_id.id)])
            local_ids = []
            expat_ids = []

            if all_slips:
                rec.env.cr.execute("SELECT distinct(id), nature_employe FROM hr_employee WHERE "
                                   "id IN (SELECT employee_id FROM hr_payslip WHERE id=ANY(%s)) "
                                   "GROUP BY nature_employe, id", (all_slips.ids,))
                result = rec.env.cr.dictfetchall()
                if result:
                    for x in result:
                        if x['nature_employe'] == 'local':
                            local_ids.append(x['id'])
                        else:
                            expat_ids.append(x['id'])
                if local_ids != []:
                    rec.env.cr.execute("SELECT sum(total) FROM hr_payslip_line WHERE slip_id=ANY(%s) AND code='BRUT'"
                                       " AND employee_id=ANY(%s)",
                                       (all_slips.ids, local_ids))
                    result = rec.env.cr.fetchone()
                    if result:
                        rec.total_brut_imposable_local = result[0] * 0.8
                if expat_ids != []:
                    rec.env.cr.execute("SELECT sum(total) FROM hr_payslip_line WHERE slip_id=ANY(%s) AND code='BRUT'"
                                       " AND employee_id=ANY(%s)",
                                       (all_slips.ids, expat_ids))
                    result = rec.env.cr.fetchone()
                    if result:
                        rec.total_brut_imposable_expat = result[0] * 0.8

    def _compute_all_total(self):
        for rec in self:
            rec.total_brut_imposable_local = 0
            rec.total_retenu_employee = 0
            rec.total_number_local = 0
            rec.total_number_expat = 0
            rec.total_ce_agricole = 0
            rec.total_cn_expat_employer = 0
            rec.total_cn_locala_employer = 0
            rec.amount_total = 0
            if rec.total_brut_imposable_expat and rec.company_id.rate_ce_expat:
                rec.total_ce_expat = rec.total_brut_imposable_expat * rec.company_id.rate_ce_expat / 100
            if rec.total_brut_imposable_expat and rec.company_id.rate_ce_agricole:
                rec.total_ce_agricole = rec.total_brut_imposable_expat * rec.company_id.rate_ce_agricole / 100
            if rec.total_brut_imposable_expat and rec.company_id.rate_its:
                rec.total_cn_expat_employer = rec.total_brut_imposable_expat * rec.company_id.rate_its / 100
            if rec.total_brut_imposable_local and rec.company_id.rate_its:
                rec.total_cn_locala_employer = rec.total_brut_imposable_local * rec.company_id.rate_its / 100
            if rec.total_ce_expat and rec.total_ce_agricole and rec.total_cn_expat_employer and rec.total_cn_locala_employer:
                rec.total_contribution_employer = rec.total_ce_expat + rec.total_ce_agricole + rec.total_cn_expat_employer \
                                                  + rec.total_cn_locala_employer
            if rec.total_contribution_employer and rec.total_retenu_employee:
                rec.amount_total = rec.total_contribution_employer + rec.total_retenu_employee
            if rec.total_cnps_employee and rec.total_its_employee and rec.total_cn and rec.total_regime_agricole + rec.total_igr_employee:
                rec.total_retenu_employee = rec.total_cnps_employee + rec.total_its_employee + rec.total_cn + \
                                            rec.total_regime_agricole + rec.total_igr_employee

    name = fields.Char('Nom', required=True, size=155)
    date_from = fields.Date('Debut mois', required=True)
    date_to = fields.Date('Fin mois', required=True)
    company_id = fields.Many2one('res.company', 'Société', default=lambda self: self.env.user.company_id.id)
    total_brut = fields.Integer("Total Brut", )
    total_avantage_nature = fields.Integer("Avantage en nature")
    total_autres = fields.Integer("Total Autres")
    revenu_net_imposable = fields.Integer("Revenu Net imposable")
    total_net_imposable = fields.Integer("Revenu Net imposable (total)")
    total_cn = fields.Integer("Contribution national")
    total_cnps_employee = fields.Integer("Total Régime retraite")
    total_igr_employee = fields.Integer("Impôt Général sur le revenu (IGR)")
    total_regime_agricole = fields.Integer("Total Régime Agricole", default=0)
    total_its_employee = fields.Integer("Impôt sur traitements, salaires, pensions, rentes viagères (IS)")
    total_retenu_employee = fields.Integer("TOTAL DES RETENUES AUX SALARIES", compute='_compute_all_total', store=True)
    total_number_local = fields.Integer("Effectif locaux", compute='_get_effectif_employee', store=True)
    total_number_expat = fields.Integer("Effectif Expatriés", compute='_get_effectif_employee', store=True)
    total_brut_imposable_local = fields.Integer("Revenu Net imposable des locaux", compute='_get_revenu_employee',
                                                store=True)
    total_brut_imposable_expat = fields.Integer("Revenu Net imposable des expatriés", compute='_get_revenu_employee',
                                                store=True)
    total_ce_expat = fields.Integer("Total CE Personnel expatrié (Régime général)", compute='_compute_all_total',
                                    store=True)
    total_ce_local = fields.Integer("Total CE Personnel Local (Régime général)", default=0)
    total_ce_agricole = fields.Integer("Total CE Régime agricole", compute='_compute_all_total', store=True)
    total_cn_expat_employer = fields.Integer("Personnel expatrié (Régime général)", compute='_compute_all_total',
                                             store=True)
    total_cn_locala_employer = fields.Integer("Personnel Local (Régime général)", compute='_compute_all_total',
                                              store=True)
    total_contribution_employer = fields.Integer("TOTAL DES CONTRIBUTIONS A LA CHARGE DE L’EMPLOYEUR",
                                                 compute='_compute_all_total', store=True)
    amount_total = fields.Integer("TOTAL A PAYER", compute='_compute_all_total', store=True)

    def compute(self):
        for rec in self:
            slip_obj = rec.env['hr.payslip']
            all_slips = slip_obj.search([('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to),
                                         ('company_id', '=', rec.company_id.id)])
            lines = []
            amount = 0
            if all_slips:
                total_brut = sum([slip.brut_imposable for slip in all_slips])
                rec.total_brut = total_brut
                revenu_net_imposable = total_brut
                rec.revenu_net_imposable = revenu_net_imposable
                total_net_imposable = revenu_net_imposable * 0.8
                rec.total_net_imposable = total_net_imposable
                rec.total_its_employee = rec.total_net_imposable * 1.5 / 100
                rec.env.cr.execute("SELECT sum(total) FROM hr_payslip_line WHERE slip_id=ANY(%s) AND code='CN'",
                                   (all_slips.ids,))
                result = rec.env.cr.fetchone()
                if result:
                    rec.total_cn = result[0]
                rec.env.cr.execute(
                    "SELECT sum(total) FROM hr_payslip_line WHERE slip_id=ANY(%s) AND code='CNPS'",
                    (all_slips.ids,))
                result = rec.env.cr.fetchone()
                if result:
                    rec.total_cnps_employee = result[0]
                rec.env.cr.execute(
                    "SELECT sum(total) FROM hr_payslip_line WHERE slip_id=ANY(%s) AND code='IGR'",
                    (all_slips.ids,))
                result = rec.env.cr.fetchone()
                if result:
                    rec.total_igr_employee = result[0]
