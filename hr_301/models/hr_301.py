# -*- conding:utf-8 -*-


from odoo import api, fields, models, _


class Hr301(models.Model):
    _name = "hr.301"
    _description = "HR 301 Management"

    name = fields.Char("Libellé")
    date_from = fields.Date('Date de début', required=True)
    date_to = fields.Date('Date de fin', required=True)
    company_id = fields.Many2one('res.company', 'Compagnie', required=True,
                                 default=lambda self: self.env.user.company_id.id)
    # account_is = fields.Many2one("account.account", "Compte Comptable associé à IS", required=False)
    # account_cn = fields.Many2one("account.account", "Compte Comptable associé à CN", required=False)
    # account_igr = fields.Many2one("account.account", "Compte Comptable associé à IGR", required=False)
    versement_ids = fields.One2many("hr.301.versement", "etat_301_id", "Versements ou à Verser", required=False)
    line_ids = fields.One2many("hr.301_line", "etat_301_id", "Lignes", required=False)
    total_employee = fields.Integer("Effectif total", compute="_getSummary")
    total_employee_local = fields.Integer("Effectif employé Local", compute="_getSummary")
    total_employee_expat = fields.Integer("Effectif employé Expatrié", compute="_getSummary")
    total_employee_agricole = fields.Integer("Effectif employé Agricole", compute="_getSummary")
    total_employee_sal_min = fields.Integer("Effectif total Salaires Min", compute="_getSummary")
    total_employee_local_sal_min = fields.Integer("Effectif employé Local Salaires Min", compute="_getSummary")
    total_employee_expat_sal_min = fields.Integer("Effectif employé Expatrié Salaires Min", compute="_getSummary")
    total_employee_agricole_sal_min = fields.Integer("Effectif employé Agricole Salaires Min", compute="_getSummary")
    total_salaire_declare = fields.Float("Total salaire déclaré", compute="_getSummary")
    total_salaire_declare_local = fields.Float("Total salaires déclarés locaux", compute="_getSummary")
    total_salaire_declare_expat = fields.Float("Total salaires déclarés expat", compute="_getSummary")
    total_salaire_declare_agricole = fields.Float("Total salaires agricoles", compute="_getSummary")
    total_salaire_ndeclare = fields.Float("Total salaires non déclarés", compute="_getSummary")
    total_salaire_ndeclare_local = fields.Float("Total salaires non déclarés locaux", compute="_getSummary")
    total_salaire_ndeclare_expat = fields.Float("Total salaires non déclarés expat", compute="_getSummary")
    total_salaire_ndeclare_agricole = fields.Float("Total salaires non agricoles", compute="_getSummary")
    total_avtg_nature_local = fields.Float("Total AVTGES natures locaux", compute="_getSummary")
    total_avtg_ature_expat = fields.Float("Total sAVTGES naturesexpat", compute="_getSummary")
    total_avtg_nature_agricole = fields.Float("Total AVTGES natures agricoles", compute="_getSummary")


    def compute(self):
        self._getDefaultData()
        return

    def _getLines(self):
        results = []
        _query = """
        SELECT 
            e.id  as employee_id,
            e.nature_employe as nature_employee,
            sum(plwds.total) as total_worked_days,
            sum(plb.total) as amount_brut_total,
            sum(pli.total) as amount_igr,
            sum(plc.total) as amount_cn,
            sum(plis.total) as amount_is
        FROM 
            (SELECT * FROM hr_payslip WHERE date_from >= %(date_from)s AND date_to <= %(date_to)s) p
            left join hr_employee e on (p.employee_id = e.id) 
            left join hr_payslip_line plwds on (plwds.employee_id = e.id and plwds.slip_id = p.id and plwds.code = 'TJRPAY')
            left join hr_payslip_line plb on (plb.employee_id = e.id and plb.slip_id = p.id and plb.code = 'BRUT')
            left join hr_payslip_line pli on (pli.employee_id = e.id and pli.slip_id = p.id and pli.code = 'IGR')
            left join hr_payslip_line plc on (plc.employee_id = e.id and plc.slip_id = p.id and plc.code = 'CN')
            left join hr_payslip_line plis on (plis.employee_id = e.id and plis.slip_id = p.id and plis.code = 'ITS')
        GROUP BY
            e.id,
            e.nature_employe
        """
        _params = {
            "date_from": self.date_from,
            "date_to": self.date_to
        }

        self.env.cr.execute(_query, _params)
        results = self.env.cr.dictfetchall()

        return results

    def computeVersementSummury(self, lines):
        if lines:
            amount_total_out = sum([x['amount_total'] for x in lines if x['amount_total'] and x['type'] == 'out'])
            amount_is_out = sum([x['amount_is'] for x in lines if x['amount_is'] and x['type'] == 'out'])
            amount_igr_out = sum([x['amount_cn'] for x in lines if x['amount_cn'] and x['type'] == 'out'])
            amount_cn_out = sum([x['amount_igr'] for x in lines if x['amount_igr'] and x['type'] == 'out'])
            local_employee_out = sum([x['amount_is'] for x in lines if x['amount_is'] and x['type'] == 'out'])
            expat_employee_out = sum([x['amount_is'] for x in lines if x['amount_is'] and x['type'] == 'out'])
            val = {
                'month': 0,
                'date': '',
                'amount_total': amount_total_out,
                'type': 'out',
                'amount_is': amount_is_out,
                'amount_cn': amount_cn_out,
                'amount_igr': amount_igr_out,
                'local_employee': local_employee_out,
                'expat_employee': expat_employee_out,
                'etat_301_id': self.id
            }

            return val

    def _getDefaultData(self):
        self.versement_ids.unlink()
        self.line_ids.unlink()
        data = []
        for i in range(12):
            val = {
                'month': i + 1,
                'date': False,
                'amount_total': 0,
                'type': 'out',
                'amount_is': 0,
                'amount_cn': 0,
                'amount_igr': 0,
                'local_employee': 0,
                'expat_employee': 0,
                'etat_301_id': self.id
            }
            data.append(val)
        print(data)

        lines = self._getLines()
        cumul_out = self.computeVersementSummury(data)
        print(cumul_out)
        if lines:
            amount_total = sum([x['amount_brut_total'] for x in lines if x['amount_brut_total']])
            amount_is = sum([x['amount_is'] for x in lines if x['amount_is']])
            amount_igr = sum([x['amount_cn'] for x in lines if x['amount_cn']])
            amount_cn = sum([x['amount_igr'] for x in lines if x['amount_igr']])
            local_employee = sum([x['amount_is'] for x in lines if x['nature_employee'] == 'local' and x['amount_is']])
            expat_employee = sum([x['amount_is'] for x in lines if x['nature_employee'] == 'expat' and x['amount_is']])
            val = {
                'month': 13,
                'date': fields.Date.today(),
                'amount_total': amount_total,
                'type': 'in',
                'amount_is': amount_is,
                'amount_cn': amount_cn,
                'amount_igr': amount_igr,
                'local_employee': local_employee,
                'expat_employee': expat_employee,
                'etat_301_id': self.id
            }
            data.append(val)
            for line in lines:
                line.update({'etat_301_id': self.id})
            print('L145 ',lines)
            self.line_ids.create(lines)
            if cumul_out:
                val = {
                    'month': 14,
                    'amount_total': amount_total - cumul_out['amount_total'],
                    'type': 'in',
                    'amount_is': amount_is - cumul_out['amount_is'],
                    'amount_cn': amount_cn - cumul_out['amount_cn'],
                    'amount_igr': amount_igr - cumul_out['amount_igr'],
                    'local_employee': local_employee - cumul_out['local_employee'],
                    'expat_employee': expat_employee - cumul_out['expat_employee'],
                    'etat_301_id': self.id
                }
                data.append(val)

        self.env['hr.301.versement'].create(data)


class Hr301Line(models.Model):
    _name = "hr.301_line"
    _description = "Line 301 management"
    _rec_name = "employee_id"

    employee_id = fields.Many2one("hr.employee", "Employé", required=True)
    nature_employee = fields.Selection([('local', 'Local'), ('expat', 'Expat')], string="Nature employé", required=False)
    total_worked_days = fields.Float("Total jours travaillés/Congés")
    amount_brut_total = fields.Float("Brut Total")
    amount_is = fields.Float("IS")
    amount_cn = fields.Float("CN")
    amount_igr = fields.Float("IGR")
    etat_301_id = fields.Many2one("hr.301", "Etat 301")


class HR301Versement(models.Model):
    _name = "hr.301.versement"
    _description = "HR 301 Versement management"

    month = fields.Integer("Mois", required=True)
    date = fields.Date("Date", required=False)
    amount_total = fields.Float("Montant global des montants versés ou à verser")
    type = fields.Selection([('out', 'Versement'), ('in', "À verser")], default=False, required=True)
    amount_is = fields.Float("IS")
    amount_cn = fields.Float("CN")
    amount_igr = fields.Float("IGR")
    local_employee = fields.Float("Employé Local")
    expat_employee = fields.Float("Employé Expatrié")
    etat_301_id = fields.Many2one("hr.301", "Etat 301")
