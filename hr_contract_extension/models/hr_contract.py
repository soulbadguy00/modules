# -*- coding: utf-8 -*-

import time
from odoo import api, fields, osv, exceptions, models
from datetime import datetime
from odoo.tools.translate import _
from odoo.exceptions import UserError, RedirectWarning, ValidationError

from dateutil.relativedelta import relativedelta


class HrTypePiece(models.Model):
    _name = "hr.type.piece"
    _description = "Type de pièce d'identité"

    name = fields.Char("Désignation", size=128, required=True)
    description = fields.Text("Description")


class HrPieceIdentite(models.Model):
    _name = "hr.piece.identite"
    _description = "Pièce d'identité"
    _rec_name = "numero_piece"

    numero_piece = fields.Char("Numéro de la pièce", size=128, required=True)
    nature_piece = fields.Selection([('attestion', "Attestation d'indentité"), ("carte_sejour", "Carte de séjour"),
                                    ("cni", "CNI"), ("passeport", "Passeport")], string="Nature", required=True)
    date_etablissement = fields.Date("Date d'établissement", required=True)
    autorite = fields.Char("Autorité", size=128)


class HrContract(models.Model):
    _inherit = "hr.contract"

    @api.onchange('employee_id')
    def _onchange_employee_id(self):
        if self.employee_id:
            self.job_id = self.employee_id.job_id
            self.department_id = self.employee_id.department_id
            self.date_start = self.employee_id.start_date


    def calcul_anciennete_actuel(self):
        anciennete = {}
        for rec in self:
            rec.ensure_one()
            this_date = today = datetime.today()
            start_date = fields.Datetime.from_string(rec.employee_id.start_date)
            if rec.date_end:
                end_date = fields.Datetime.from_string(rec.date_end)
                this_date = min(today, end_date)
            tmp = relativedelta(this_date, start_date) + relativedelta(months=+rec.mois_report, years=+ rec.an_report)
            anciennete = {
                'year_old': tmp.years,
                'month_old': tmp.months,
            }
            return anciennete


    def _get_anciennete(self):
        res = {}
        for rec in self:
            anciennete = rec.calcul_anciennete_actuel()
            if anciennete:
                rec.an_anciennete = anciennete['year_old']
                rec.mois_anciennete = anciennete['month_old']

    expatried = fields.Boolean('Expatrié', default=False)
    an_report = fields.Integer('Année report ancienneté')
    mois_report = fields.Integer('Mois report')
    an_anciennete = fields.Integer("Nombre d'année", compute='_get_anciennete', store=True)
    mois_anciennete = fields.Integer('Nombre de mois', compute='_get_anciennete', store=True)
    anne_anc = fields.Integer('Année ancienneté')
    sursalaire = fields.Integer('Sursalaire', required=False)
    hr_convention_id = fields.Many2one('hr.convention', "Convention", required=False)
    hr_secteur_id = fields.Many2one('hr.secteur.activite', "Secteur d'activité", required=False)
    categorie_salariale_id = fields.Many2one('hr.categorie.salariale', 'Catégorie salariale', required=False)
    hr_payroll_prime_ids = fields.One2many("hr.payroll.prime.montant", 'contract_id', "Primes")
    type_ended = fields.Selection([('licenced', 'Licencement'), ('hard_licenced', 'Licencement faute grave'),
                                   ('ended', 'Fin de contract')], 'Type de clôture', index=True)
    description_cloture = fields.Text("Motif de Clôture")
    wage = fields.Integer('Salaire de base', required=True)
    notify_model_id = fields.Many2one('notify.model', 'Modèle de notification', required=False)
    notif_ids = fields.One2many('notif.line', 'res_id', 'lignes')
    model_contract_id = fields.Many2one('hr.model.contract', "Modèle de contrat", required=False)
    struct_id = fields.Many2one("hr.payroll.structure","Structure salariale")


    def limitDigit(self):
        yearNumber = self.an_report
        if yearNumber and len(str(abs(yearNumber)))>3:
            raise ValidationError(_('Number of digits must on exceed 2'))

    @api.onchange('model_contract_id')
    @api.depends('model_contract_id')
    def onChaneContractModel(self):
        self.job_id = self.model_contract_id.titre_poste.id
        self.hr_convention_id = self.model_contract_id.convention_id.id
        self.hr_secteur_id = self.model_contract_id.secteur_activite_id.id
        self.categorie_salariale_id = self.model_contract_id.categorie_salariale.id
        self.type_id = self.model_contract_id.type_contract.id
        self.struct_id = self.model_contract_id.structure_salariale.id
        primes = []
        print('L110', self.model_contract_id.prime_ids)
        for prime in self.model_contract_id.prime_ids:
            prime_values = {
                'prime_id': prime.prime_id.id,
                'montant_prime': prime.montant_prime,
                'contract_id': self.id,
            }
            primes.append(prime_values)
        if primes:
            self.hr_payroll_prime_ids.unlink()
        self.hr_payroll_prime_ids.create(primes)

    @api.onchange('notify_model_id')
    def compute_notification(self):
        print(self._context)
        self.ensure_one()
        notif_model = self.env['notif.line']
        if self.date_end :
            print("le contract est %s et prend fin le %s"%(self.date_end, self.id))
            date = fields.Datetime.from_string(self.date_end)
            params = self._context.get('params')
            print(params)
            for line in self.notify_model_id.line_ids :
                notif_model.generate_notification_line(self.name, self.id, line, date)


    def validate_contract(self):
        for rec in self:
            return rec.write({'state': 'open'})


    def closing_contract(self):
        for rec in self:
            view_id = rec.env['ir.model.data'].get_object_reference('hr_contract_extension', 'hr_contract_closed_form_view')
            return {
                    'name':_("Clôture de contrat"),
                    'view_mode': 'form',
                    'view_id': view_id[1],
                    'view_type': 'form',
                    'res_model': 'hr.contract.closed',
                    'type': 'ir.actions.act_window',
                    'nodestroy': True,
                    'target': 'new',
                    'domain': '[]',
                    'context': self._context,
                }


    def action_cancel(self):
        for rec in self:
            return rec.write({'state':'cancel'})

    @api.onchange('hr_convention_id')
    def on_change_convention_id(self):
        if self.hr_convention_id :
            return {'domain':{'hr_secteur_id':[('hr_convention_id','=',self.hr_convention_id.id)]}}
        else :
            return {'domain':{'hr_secteur_id':[('hr_convention_id','=',False)]}}

    @api.onchange('hr_secteur_id')
    def on_change_secteur_id(self):
        if self.hr_secteur_id :
            return {'domain':{'categorie_salariale_id':[('hr_secteur_activite_id','=', self.hr_secteur_id.id)]}}
        else :
            return {'domain':{'categorie_salariale_id':[('hr_secteur_activite_id','=',False)]}}


    @api.onchange('categorie_salariale_id')
    def on_change_categorie_salariale_id(self):
        if self.categorie_salariale_id:
            self.wage= self.categorie_salariale_id.salaire_base


class hr_payroll_prime(models.Model):
    _name = "hr.payroll.prime"
    _description = "prime"

    name = fields.Char('name', size=64, required=True)
    code = fields.Char('Code', size=64, required=True)
    description = fields.Text('Description')


class hr_payroll_prime_montant(models.Model):
    _name = "hr.payroll.prime.montant"
    _description = "hr payroll montant"

    @api.depends('prime_id')
    def _get_code_prime(self):
        for rec in self:
            if rec.prime_id:
                rec.code = rec.prime_id.code

    name = fields.Char("Prime montant")
    prime_id = fields.Many2one('hr.payroll.prime', 'prime', required=True)
    code = fields.Char("Code", compute='_get_code_prime',store = True)
    contract_id = fields.Many2one('hr.contract', 'Contract')
    montant_prime = fields.Integer('Montant', required=True)


class HrContractType(models.Model):

    _inherit = "hr.payroll.structure.type"
    _description = "hr contract type"

    code = fields.Char("Code", size=5 )
