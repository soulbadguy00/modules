# -*- coding:utf -*-


from odoo import api, fields, models, _


class ResCompany(models.Model):
    _inherit = "res.company"


    def _getTotalCGRAE(self):
        for res in self:
            total = res.tx_cgrae_employee + res.tx_cgrae_employer
            res.tx_cgrae_total = total

    tx_cgrae_employee = fields.Float("Taux CGARE employé", default=8.33)
    tx_cgrae_employer = fields.Float("Taux CGRAE Employeur", default=16.67)
    tx_cgrae_total = fields.Float("Total taux CGRAE", compute="_getTotalCGRAE")