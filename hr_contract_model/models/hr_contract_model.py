# -*- coding: utf-8 -*-

from odoo import api, models, osv,fields
# from openerp import osv,fields,models, api
from odoo.tools.translate import _
from datetime import datetime


class ModelContract(models.Model):
    _name = "hr.model.contract"
    _description = "Modèle de contrat"

    @api.onchange('convention_id')
    def on_change_convention_id(self):
        if self.convention_id :
            return {
                'domain':
                    {
                        'hr_secteur_id':
                            [('hr_convention_id', '=', self.convention_id.id)]
                    }
            }
        else:
            return {
                'domain':
                    {'hr_secteur_id':
                         [('hr_convention_id', '=', False)]
                     }
            }

    @api.onchange('secteur_activite_id')
    def on_change_secteur_id(self):
        if self.secteur_activite_id :
            return {
                'domain':
                    {
                        'categorie_salariale':
                            [('hr_secteur_activite_id', '=', self.secteur_activite_id.id)]
                    }
            }
        else:
            return {
                'domain':
                    {
                        'categorie_salariale':
                            [('hr_secteur_activite_id', '=', False)]
                    }
            }
        


    @api.onchange('categorie_salariale')
    def change_categorie(self):
        res = {'value':{
                      'salaire_base':0,
                      }
            }
        if self.categorie_salariale and self.categorie_salariale.salaire_base:
            self.salaire_base= self.categorie_salariale.salaire_base
        else :
            self.salaire_base= 0

    name= fields.Char("Designation",size=128,required=True)
    salaire_base= fields.Integer("Salaire de base",required=True)
    prime_ids= fields.One2many("hr.payroll.prime.montant","model_contract_id","Primes")
    categorie_salariale= fields.Many2one("hr.categorie.salariale","Categorie salariale",required=True,
             domain="[('hr_secteur_activite_id', '=', secteur_activite_id)]")
    titre_poste= fields.Many2one("hr.job","Titre du Poste",required=False)
    type_contract= fields.Many2one("hr.model.contract.type","Type de contrat",required=True)
    structure_salariale= fields.Many2one('hr.payroll.structure',"Structure salariale",required=True)
    convention_id= fields.Many2one("hr.convention","Convention",required=True)
    secteur_activite_id= fields.Many2one("hr.secteur.activite","Secteur d'activité",required=True)


class ContractGenerator(models.Model):
    _name = "hr.contract.generate"
    _description = "hr contract generate"

    def generate_contract(self):
        for rec in self:
            print('L81', rec)
            contract_obj = rec.env["hr.contract"]
            prime_obj= rec.env['hr.payroll.prime.montant']
            for employee in rec.employee_ids:
                vals={
                  'name': "Contract %s"%employee.name,
                  "wage": rec.model_contract_id.salaire_base,
                  "employee_id":employee.id,
                  "sursalaire": 0,
                  "categorie_salariale_id": rec.model_contract_id.categorie_salariale.id,
                  'job_id': rec.model_contract_id.titre_poste.id,
                  'struct_id': rec.model_contract_id.structure_salariale.id,
                  'hr_convention_id': rec.model_contract_id.convention_id.id,
                  'hr_secteur_id': rec.model_contract_id.secteur_activite_id.id,
                  'type_id': rec.model_contract_id.type_contract.id,
                }
                print('vals(contract) ', vals)

                contract = contract_obj.create(vals)
                for prime in rec.model_contract_id.prime_ids :
                    prime_values={
                              'prime_id':prime.prime_id.id,
                              'montant_prime':prime.montant_prime,
                              'contract_id':contract.id,
                              }
                    prime_montant_id = prime_obj.create(prime_values)
                    print('vals prime ', prime_values)

    name = fields.Char("Name",size=128,required=True)
    model_contract_id = fields.Many2one("hr.model.contract",'Model',required=True)
    date_generate = fields.Datetime("Date de génération")
    employee_ids = fields.Many2many("hr.employee","hr_model_contract_rel","hr_model_contract_id","employee_id","Employees")


class hr_payroll_prime_montant(models.Model):
    _inherit = 'hr.payroll.prime.montant'

    model_contract_id= fields.Many2one("hr.model.contract","Modèle de contrat")


class ContractType(models.Model):

    _name = 'hr.model.contract.type'
    _description = 'Contract Type'
    _order = 'sequence, id'

    name = fields.Char(string='Contract Type', required=True, translate=True)
    sequence = fields.Integer(help="Gives the sequence when displaying a list of Contract.", default=10)


class Contract(models.Model):
    _inherit = "hr.contract"

    type_id = fields.Many2one("hr.model.contract.type","Type de contrat")

    def get_all_structures(self):
        """
        @return: the structures linked to the given contracts, ordered by hierachy (parent=False first,
                 then first level children and so on) and without duplicata
        """
        structures = self.mapped('structure_type_id')
        if not structures:
            return []
        # YTI TODO return browse records
        return list(set(structures._get_parent_structure().ids))
