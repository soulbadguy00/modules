# -*- coding:utf-8 -*-


from odoo import api, fields, models, _
from itertools import groupby
from odoo.tools import format_amount


class HrTransferOrder(models.Model):
    _name = "hr.tansfer.order"
    _description = "transfer order manager"



    @api.depends('order_line_ids')
    def _get_total_amount(self):
        for rec in self:
            total = sum([x.amount for x in rec.order_line_ids])
            rec.total = total

    name = fields.Char("Libellé", required=True)
    date_from = fields.Date("Date début", required=True)
    date_to = fields.Date("Date fin", required=True)
    company_id = fields.Many2one('res.company', 'Société', default=lambda self: self.env.user.company_id.id)
    order_line_ids = fields.One2many('hr.transfer.order_line', 'transfer_order_id', 'lignes')
    order_comment_ids = fields.One2many('hr.transfer.order.comment', 'transfer_order_id', 'Commentaires')
    total = fields.Integer('Total général', compute="_get_total_amount", store=True)
    groupby_bank = fields.Boolean("Grouper par banques", default=False)


    def compute(self):
        for rec in self:
            context = rec._context
            datas = {'ids': rec.id}
            datas['model'] = rec._name
            rec.order_line_ids.unlink()
            payslips = rec.env['hr.payslip'].search([('company_id', '=', rec.company_id.id),
                                                     ('date_from', '>=', rec.date_from),
                                                   ('date_to', '<=', rec.date_to),
                                                     ('state','=','verify')])
            res = []
            comment_res = []
            if payslips:
                num_order = 1
                for slip in payslips:
                    amount_order = 0

                    slip_amount = slip.get_amount_rubrique('NET')
                    if slip.employee_id.dispatch_bank_ids:
                        for x in slip.employee_id.dispatch_bank_ids:
                            if x.type == 'fix':
                                amount_order += x.amount
                        if amount_order < slip_amount:
                            balance = slip_amount - amount_order
                            for d_bank in slip.employee_id.dispatch_bank_ids:

                                val = {
                                    'transfer_order_id': self.id,
                                    'num_order': num_order,
                                    'employee_id': slip.employee_id.id,
                                    'bank_id': d_bank.bank_id.bank_id.id,
                                    'acc_bank_id': d_bank.bank_id.id,
                                    'amount': d_bank.amount
                                }
                                if d_bank.type == 'balance':
                                    val['amount'] = balance
                                res.append(val)
                                num_order += 1
                        else:
                            c_vals = {
                                'employee_id': slip.employee_id.id,
                                'comment': "Le montant reparti est supérieur au net a payé du bulletin de salaire."
                            }
                            comment_res.append(c_vals)
                    else:
                        val = {
                            'transfer_order_id': self.id,
                            'num_order': num_order,
                            'employee_id': slip.employee_id.id,
                            'acc_bank_id': slip.employee_id.main_bank_id.id,
                            'bank_id': slip.employee_id.main_bank_id.bank_id.id ,
                            'amount': slip_amount
                        }
                        res.append(val)
                        num_order += 1
            rec.order_line_ids.create(res)
            rec.order_comment_ids.create(comment_res)
            #report_pages = self.bank_group_line()


    def bank_group_line(self):
        """
        Returns this order lines classified by sale_layout_category and separated in
        pages according to the category pagebreaks. Used to render the report.
        """
        for rec in self:
            rec.ensure_one()
            report_pages = [[]]
            for bank, lines in groupby(rec.order_line_ids, lambda l: l.bank_id):
                # If last added category induced a pagebreak, this one will be on a new page
                if report_pages[-1] and report_pages[-1][-1]['pagebreak']:
                    report_pages.append([])
                # Append category to current report page
                val = {
                        'name': bank and bank.name or _('Uncategorized'),
                        'pagebreak': '',
                        'lines': list(lines),
                }
                report_pages[-1].append(val)
            return report_pages

    def format_amount(self, amount):
        return format_amount.manageSeparator(amount)


class HrTransferOrderLine(models.Model):
    _name = 'hr.transfer.order_line'
    _description = "order line managment"
    _order = "bank_id"

    num_order = fields.Integer("N° ordre")
    employee_id = fields.Many2one('hr.employee', 'Employé', required=True)
    acc_bank_id = fields.Many2one('res.partner.bank', 'Compte bancaire', required=False)
    bank_id = fields.Many2one('res.bank', "Banque", required=False)
    amount = fields.Integer("Salaire")
    transfer_order_id = fields.Many2one('hr.tansfer.order', 'Ordre de transfert', required=False)


class HrTransferOrderComment(models.Model):
    _name = "hr.transfer.order.comment"
    _description = "Transfer Comment Manager"

    employee_id = fields.Many2one("hr.employee", "Employé", required=True)
    comment = fields.Char("Commentaire")
    transfer_order_id = fields.Many2one('hr.tansfer.order', 'Ordre de transfert', required=False)
