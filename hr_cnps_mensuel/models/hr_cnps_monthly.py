# -*- coding:utf-8 -*-


from odoo import api, fields, _, models
from . import hr_cnps_settings
from itertools import groupby


class HrCnpsMonthly(models.Model):
    _name = "hr.cnps.monthly"
    _description = "CNPS Mensuel"

    @api.depends("line_ids", "cotisation_ids", "other_line_ids")
    def _get_total(self):
        for rec in self:
            if rec.line_ids:
                total_employee = sum([line.salaries_number for line in rec.line_ids])
                total_assiette_cnps = sum([line.regime_retraite for line in rec.line_ids])
                total_assiette_other = sum([line.regime_autre for line in rec.line_ids])
                rec.total_employee = total_employee
                rec.total_assiette_cnps = total_assiette_cnps
                rec.total_assiette_other = total_assiette_other
            if rec.cotisation_ids:
                total = sum([x.amount_contributed for x in rec.cotisation_ids])
                rec.total_cotisation_contributed = total
            if rec.other_line_ids:
                total_brut = sum([x.amount_brut for x in rec.other_line_ids])
                rec.total_salaire_brut = total_brut

    name = fields.Char("Libellé", required=True)
    date_from = fields.Date("Date de début", required=True)
    date_to = fields.Date("Date de fin", required=True)
    slip_ids = fields.Many2many('hr.payslip', string="Bulletins de paie")
    slips_count = fields.Integer("Nombre de bulletins de paie", compute='_compute_slips_count', store=True)
    company_id = fields.Many2one('res.company', "Société", default=lambda self: self.env.user.company_id.id)
    total_employee = fields.Integer("Nombre total d'employés", compute='_get_total', store=True)
    total_assiette_cnps = fields.Float("Total assiette CNPS", compute='_get_total', store=True, digits=(12, 0))
    total_assiette_other = fields.Float('Autre total assiette', compute='_get_total', store=True, digits=(12, 0))
    total_cotisation_contributed = fields.Float('Montant total cotisation', compute='_get_total', store=True,
                                                digits=(12, 0))
    total_salaire_brut = fields.Float("Total salaires bruts payes", digits=(12, 0), compute='_get_total', store=True)
    line_ids = fields.One2many('hr.cnps.monthly.category_line', 'cnps_monthly_id', 'Lignes')
    other_line_ids = fields.One2many('hr.cnps.monthly.line', 'cnps_monthly_id', "Les elements")
    cotisation_ids = fields.One2many("hr.cnps.cotisation.line", "cnps_monthly_id", "Decomptes de cotisations")
    type_employe = fields.Selection([('h', 'Horaire'), ('j', 'Journalier'), ('m', 'Mensuel'),
                                     ('all', 'Tous les employés')], "Livre de paie pour ", default="all")

    @api.depends('slip_ids')
    def _compute_slips_count(self):
        for rec in self:
            rec.slips_count = len(rec.slip_ids)

    def compute(self):
        for rec in self:
            rec.line_ids.unlink()
            rec.other_line_ids.unlink()
            rec.cotisation_ids.unlink()
            res = []
            slip_obj = rec.env['hr.payslip']
            all_slips = slip_obj.search([('date_from', '>=', rec.date_from), ('date_to', '<=', rec.date_to),
                                         ('company_id', '=', rec.company_id.id)])
            if rec.type_employe != 'all':
                all_slips = all_slips.filtered(lambda slip: slip.type == rec.type_employe)
            lines = []
            cotisations = []
            type_cnps = rec.env['hr.cnps.setting'].search([])
            if all_slips:
                rec.env.cr.execute("SELECT distinct(employee_id) FROM hr_payslip WHERE id=ANY(%s)", (all_slips.ids,))
                results = rec.env.cr.fetchall()
                if results:
                    employee_ids = [x[0] for x in results]
                    rec.env.cr.execute(""
                                       "SELECT distinct(employee_id) as employee_id, sum(brut_imposable) as "
                                       "brut_imposable,AVG(base_daily) as base_jour FROM hr_payslip "
                                       "WHERE id=ANY(%s) AND  employee_id=ANY(%s) GROUP BY"
                                       " employee_id", (all_slips.ids, employee_ids))
                    data = rec.env.cr.dictfetchall()
                    if data:
                        for tcnps in type_cnps:
                            l_vals = {
                                'cnps_monthly_id': self.id,
                                'name': tcnps.name,
                                'salaries_number': 0,
                                'regime_retraite': 0,
                                'regime_autre': 0
                            }
                            for dt in data:
                                found = False
                                employee = rec.env['hr.employee'].browse(dt['employee_id'])
                                if employee:
                                    if tcnps.type != 'm':
                                        if employee.type == tcnps.type:
                                            if tcnps.amount_min < dt['base_jour'] <= tcnps.amount_max:
                                                found = True
                                    else:
                                        if employee.type == tcnps.type:
                                            if tcnps.amount_min < dt['brut_imposable'] <= tcnps.amount_max:
                                                found = True
                                if found:
                                    l_vals['salaries_number'] += 1
                                    val = {
                                        'cnps_monthly_id': self.id,
                                        'employee_id': employee.id,
                                        'type': employee.type,
                                        'amount_brut': dt['brut_imposable'],
                                        'daily_basis': dt['base_jour'],
                                        'tranche_id': tcnps.id,
                                        'date_start': rec.date_from,
                                        'date_to': rec.date_to
                                    }
                                    if dt['brut_imposable'] < rec.company_id.max_assiette_cnps:
                                        val['assiette_cnps'] = dt['brut_imposable']
                                    else:
                                        val['assiette_cnps'] = rec.company_id.max_assiette_cnps
                                    l_vals['regime_retraite'] += val['assiette_cnps']
                                    if dt['brut_imposable'] < rec.company_id.max_assiette_autre_contribution:
                                        val['assiette_other'] = dt['brut_imposable']
                                    else:
                                        val['assiette_other'] = rec.company_id.max_assiette_autre_contribution

                                    val['assurance_maternite_amount'] = val['assiette_other'] * rec.company_id. \
                                        taux_assurance_mater / 100
                                    val['prestation_family_amount'] = val['assiette_other'] * rec.company_id. \
                                        taux_prestation_familiale / 100
                                    val['accident_travail_amount'] = val['assiette_other'] * rec.company_id. \
                                        taux_accident_travail / 100
                                    if employee.nature_employe == 'local':
                                        val['cnps_amount'] = val['assiette_cnps'] * \
                                                             (rec.company_id.taux_cnps_employee_local) / 100
                                    else:
                                        val['cnps_amount'] = val['assiette_cnps'] * \
                                                             (rec.company_id.taux_cnps_employe_expat) / 100
                                    val['cnps_amount'] += val['assiette_cnps'] * \
                                                          (rec.company_id.taux_cnps_employer) / 100
                                    l_vals['regime_autre'] += val['assiette_other']
                                    res.append(val)
                            lines.append(l_vals)
                rec.line_ids.create(lines)
                rec.other_line_ids.create(res)
                templates = rec.env['hr.cnps.cotisation.line.template'].search([('company_id', '=', rec.company_id.id)])
                if templates:
                    for tpl in templates:
                        tpl_val = {
                            'cnps_monthly_id': self.id,
                            'name': tpl.name,
                            'taux': tpl.taux,
                        }
                        if tpl.type == 'cnps':
                            tpl_val['amount_submitted'] = rec.total_assiette_cnps
                        else:
                            tpl_val['amount_submitted'] = rec.total_assiette_other
                        tpl_val['amount_contributed'] = tpl_val['amount_submitted'] * tpl.taux / 100
                        cotisations.append(tpl_val)
                    rec.cotisation_ids.create(cotisations)

            return True

    def export_xls(self):
        for rec in self:
            context = rec._context
            rec.ensure_one()
            data = {}
            data['ids'] = rec.id
            data['model'] = rec._name
            return rec.env.ref('hr_cnps_mensuel.hr_cnps_report_xlsx').report_action(rec, data=data)


class HrCnpsMonthlyLine(models.Model):
    _name = 'hr.cnps.monthly.line'
    _description = "CNPS mensuel line"
    _order = "employee_id"

    employee_id = fields.Many2one('hr.employee', 'Employé', required=True)
    type = fields.Selection(hr_cnps_settings.Type_employee, 'Type', required=False, default=False)
    tranche_id = fields.Many2one('hr.cnps.setting', 'Tranche')
    amount_brut = fields.Float("Salaire brut", digits=(12, 0))
    assiette_cnps = fields.Float("Assiette CNPS", digits=(12, 0))
    assiette_other = fields.Float("Assiette pour autres prélèvements", digits=(12, 0))
    daily_basis = fields.Float("Base journalière", digits=(12, 0))
    cnps_amount = fields.Float("Montant CNPS", digits=(12, 0))
    assurance_maternite_amount = fields.Float("Montant Assurance maternité", digits=(12, 0))
    prestation_family_amount = fields.Float("Montant Prestation familiale", digits=(12, 0))
    accident_travail_amount = fields.Float("Montant Accident de travail", digits=(12, 0))
    cnps_monthly_id = fields.Many2one("hr.cnps.monthly", "CPNS mensuel", required=False)
    date_start = fields.Date("Date de début")
    date_to = fields.Date("Date de fin")


class HrCnpsMonthlyCategoryLine(models.Model):
    _name = "hr.cnps.monthly.category_line"
    _description = "hr cnps monthly categorie line"

    name = fields.Char("Designation", required=True)
    salaries_number = fields.Integer("Nombre de salaries", required=True)
    regime_retraite = fields.Float("Regime de retraite", digits=(12, 0))
    regime_autre = fields.Float("Autre regime", digits=(12, 0))
    cnps_monthly_id = fields.Many2one("hr.cnps.monthly", "CNPS Mensuel", required=False)


class HrCnpsCotisationLine(models.Model):
    _name = "hr.cnps.cotisation.line"
    _description = "hr cnps cotisation line"

    name = fields.Char("Designation", required=True)
    amount_submitted = fields.Float("salaires soumis à cotisation", digits=(12, 0))
    taux = fields.Float("Taux")
    amount_contributed = fields.Float("Montant", digits=(12, 0))
    cnps_monthly_id = fields.Many2one("hr.cnps.monthly", "CNPS Mensuel", required=False)
