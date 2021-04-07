# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrCGRAE(models.TransientModel):
    _name = "hr_cmu.cmu_rapport"
    _description = "Gestion des rapports CMU"

    def compute(self):
        data = []
        for rec in self:
            rec.env.cr.execute(
                "SELECT employee_id FROM hr_payslip WHERE date_from >= %s AND date_to <= %s AND company_id = %s",
                (rec.date_from, rec.date_to, rec.company_id.id))
            results = rec.env.cr.fetchall()
            if results:
                employee_ids = [x[0] for x in results]
                if employee_ids:
                    employees = rec.env['hr.employee'].browse(employee_ids)
                    for emp in employees:
                        val = {
                            'cmu_id': self.id,
                            'num_cnps': emp.matricule_cnps,
                            'num_cmu': emp.num_cmu,
                            'type': 't',
                            'name': emp.name,
                            'first_name': emp.first_name,
                            'gender': emp.gender
                        }
                        data.append(val)
                        if emp.marital == 'married':
                            val = {
                                'cmu_id': self.id,
                                'num_cnps': emp.matricule_cnps,
                                'num_cmu': emp.num_cmu_conjoint,
                                'type': 'c',
                                'name': emp.conjoint_name,
                                'first_name': emp.conjoint_first_name,
                                'gender': emp.gender_conjoint
                            }
                            data.append(val)
                        if emp.enfants_ids:
                            for enf in emp.enfants_ids:
                                val = {
                                    'cmu_id': self.id,
                                    'num_cnps': emp.matricule_cnps,
                                    'num_cmu': enf.num_cmu,
                                    'type': 'e',
                                    'name': enf.name,
                                    'first_name': enf.first_name,
                                    'gender': enf.gender
                                }
                                data.append(val)
            if data:
                rec.line_ids.unlink()
                rec.line_ids.create(data)
            return data

    name = fields.Char('Libellé')
    date_from = fields.Date('Date de début', required=True)
    date_to = fields.Date('Date de fin', required=True)
    company_id = fields.Many2one('res.company', 'Compagnie', required=True,
                                 default=lambda self: self.env.user.company_id.id)
    line_ids = fields.One2many("hr_cmu.cmu_line", "cmu_id", "Lignes")

    def export_xls(self):
        context = self._context
        self.ensure_one()
        datas = {'ids': self.ids}
        datas['model'] = 'hr_cmu.cmu_rapport'
        print('L73 datas',datas)
        return self.env.ref('hr_cmu.report_cmu_rapport').with_context(data=datas).report_action(self, data=datas,
                                                                                                config=False)
        # return self.env['ir.actions.report'].get_action(self, 'hr_cmu.report_cmu_rapport.xlsx', data=datas)


class HrCGRAELine(models.TransientModel):
    _name = "hr_cmu.cmu_line"
    _description = "Ligne CMU management"

    num_cnps = fields.Char("Numéro CNPS")
    num_cmu = fields.Char("N° de sécurité sociale")
    type = fields.Selection([('t', 'T'), ('c', 'C'), ('e', 'E')], "Type bénéficiaire")
    name = fields.Char("Nom du bénéficiaire")
    first_name = fields.Char("Prénoms du bénéficiaire")
    gender = fields.Selection([('male', 'H'), ('female', 'F')], "Genre du bénéficiaire")
    cmu_id = fields.Many2one("hr_cmu.cmu_rapport", "CMU", required=False)