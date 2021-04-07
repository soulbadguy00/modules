#-*- coding:utf-8 -*-

from odoo import fields, models, api,exceptions


class HrReverseContract(models.TransientModel):
	_name='hr.reverse.contract'
	_description = 'Calcul inverse du salaire'

	name = fields.Selection([('brut', 'Par le brut'),('net','Par le net')], 'Méthode de calcul', requred=True)
	montant = fields.Integer('Montant du calcul', required=True)
	prime_ids = fields.One2many('hr.reverse.prime', 'hr_reverse_contract_id', 'Primes', required=True)
	hr_convention_id= fields.Many2one('hr.convention',"Convention",required=True)
	hr_secteur_id= fields.Many2one('hr.secteur.activite',"Secteur d'activité",required=True)
	categorie_salariale_id= fields.Many2one('hr.categorie.salariale', 'Catégorie salariale', required=True)
	wage = fields.Float('Salaire de Base', required=True)
	sursalaire = fields.Integer("Sursalaire", required=False)
	prime_anciennete = fields.Integer("Prime d'anciennété")


	@api.onchange("hr_convention_id")
	def on_change_convention_id(self):
	    if self.hr_convention_id :
	        return {'domain':{'hr_secteur_id':[('hr_convention_id','=',self.hr_convention_id.id)]}}
	    else :
	        return {'domain':{'hr_secteur_id':[('hr_convention_id','=',False)]}}

	@api.onchange("hr_secteur_id")
	def on_change_secteur_id(self):
	    if self.hr_secteur_id :
	        return {'domain':{'categorie_salariale_id':[('hr_secteur_activite_id','=', self.hr_secteur_id.id)]}}
	    else :
	        return {'domain':{'categorie_salariale_id':[('hr_secteur_activite_id','=',False)]}}


	@api.onchange('categorie_salariale_id')
	def on_change_categorie_salariale_id(self):
	    if self.categorie_salariale_id:
	        self.wage= self.categorie_salariale_id.salaire_base


	def compute(self):
		for rec in self:
			hr_contract_obj = rec.env['hr.contract']
			total_intrant = rec.wage
			for prime in rec.prime_ids :
				total_intrant+= prime.montant_prime

			if total_intrant > rec.montant :
				raise exceptions.Warning('Le montant est inféreur aux intrants')
			else :
				prime_anciennete = 0.0
				if rec.name == 'brut':
					contract_id = rec.env.context['active_id']
					contract= hr_contract_obj.browse(contract_id)
					if 1 < contract.an_anciennete < 26:
						prime_anciennete = 0.01 * rec.wage * contract.an_anciennete
						rec.prime_anciennete = prime_anciennete
						total_intrant+=prime_anciennete
						sursalaire = rec.montant - total_intrant
						rec.sursalaire = sursalaire

						# raise exceptions.Warning(sursalaire)



class HrReversePrime(models.TransientModel):
	_name = 'hr.reverse.prime'
	_description = "hr reverse prime"

	prime_id= fields.Many2one('hr.payroll.prime','prime',required=True)
	hr_reverse_contract_id= fields.Many2one('hr.reverse.contract','Contract')
	montant_prime= fields.Integer('Montant', required=True)



	@api.depends('prime_id')
	def _get_code_prime(self):
		for rec in self:
			if rec.prime_id:
				rec.code = rec.prime_id.code


__author__ = 'lekaizen'
