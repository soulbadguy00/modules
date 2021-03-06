# -*- encoding: utf-8 -*-

##############################################################################
#
# Copyright (c) 2012 Rodolphe Agnero - support.Rodolphe Agnero.net
# Author: Rodolphe Agnero
#
# Fichier du module hr_emprunt
# ##############################################################################  -->
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from datetime import date
from odoo import fields, models, api, _

Type_employee = [('h', 'Horaire'), ('j', 'Journalier'), ('m', 'Mensuel')]


class hr_employee_degree(models.Model):
    _name = "hr.employee.degree"
    _description = "Degree of employee"

    name = fields.Char('Name', required=True, translate=True)
    sequence = fields.Integer('Sequence', help="Gives the sequence order when displaying a list of degrees.", default=1)

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The name of the Degree of employee must be unique!')
    ]


class licence(models.Model):
    _name = "hr.licence"
    _description = "Licence employé"

    name = fields.Char('Libellé Licence', size=64, required=True, readonly=False)
    reference = fields.Char('Reférence', size=64, required=False, readonly=False)
    date_debut = fields.Date('Début validité')
    date_fin = fields.Date('Fin validité')
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)


class domaine(models.Model):
    _name = "hr.diplomes.domaine"
    _description = "Domaine de diplome employe"
    _rec_name = 'libelle'

    libelle = fields.Char('Libellé Domaine', size=64, required=True, readonly=False)


class diplome_employe(models.Model):
    _name = "hr.diplomes.employee"
    _description = "Diplome employe"

    name = fields.Char('Name', size=64, required=False, readonly=False, translate=True)
    diplome_id = fields.Many2one('hr.employee.degree', 'Niveau', required=True)
    domaine_id = fields.Many2one('hr.diplomes.domaine', 'Domaines', required=False, readonly=False)
    reference = fields.Char('Reférence', size=64, required=False, readonly=False)
    date_obtention = fields.Date("Date d'obtention")
    date_start = fields.Date("Date début")
    date_end = fields.Date("Date fin")
    type = fields.Selection([('diplome', 'Diplôme'), ('certif', 'Certification')], "Type", index=True)
    image = fields.Binary('Image')
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)


class visa(models.Model):
    _name = "hr.visa"
    _description = "visa employé"

    name = fields.Char('Libellé visa', size=64, required=True, readonly=False)
    reference = fields.Char('N° Visa', size=64, required=True, readonly=False)
    pays_id = fields.Many2one('res.country', 'Pays', required=True)
    date_debut = fields.Datetime('Début validité')
    date_fin = fields.Datetime('Fin validité')
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)


class carte_sejour(models.Model):
    _name = "hr.carte.sejour"
    _description = "Carte de séjour employé"

    name = fields.Char('Libellé visa', size=64, required=False, readonly=False)
    reference = fields.Char('N° Visa', size=64, required=False, readonly=False)
    pays_id = fields.Many2one('res.country', 'Pays', required=False)
    date_debut = fields.Datetime('Début validité')
    date_fin = fields.Datetime('Fin validité')
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)


class enfants_employe(models.Model):
    _name = "hr.employee.enfant"
    _description = "Enfants de l'employé"

    @api.depends('date_naissance')
    def _get_age_child(self):
        this_date = fields.Datetime.now()
        for child in self:
            date_naissance = fields.Datetime.from_string(child.date_naissance)
            tmp = relativedelta(this_date, date_naissance)
            child.age = tmp.years

    def name_get(self):
        result = []
        for enf in self:
            if enf.first_name:
                name = enf.name + ' ' + enf.first_name
            else:
                name = enf.name
            result.append((enf.id, name))
        return result

    name = fields.Char('Nom', size=128, required=True, readonly=False)
    first_name = fields.Char("Prénoms", size=225, required=True, readonly=False)
    date_naissance = fields.Date("Date de naissance", required=True)
    mobile = fields.Char('Portable', size=128, required=False, readonly=False)
    email = fields.Char('email', size=128, required=False, readonly=False)
    num_cmu = fields.Char("N° CMU", required=False)
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)
    age = fields.Integer('Âge', compute="_get_age_child")
    gender = fields.Selection([('male', 'M'), ('female', 'F')], "Sexe")


class HrParentEmployee(models.Model):
    _name = "hr.parent.employe"
    _description = "les parents de l'employee"

    def name_get(self):
        result = []
        for parent in self:
            if parent.first_name:
                name = parent.name + ' ' + parent.first_name
            else:
                name = parent.name
            result.append((parent.id, name))
        return result

    name = fields.Char('Nom', size=128, required=True, readonly=False)
    first_name = fields.Char("Prénoms", size=225, required=True, readonly=False)
    date_naissance = fields.Date("Date de naissance")
    mobile = fields.Char('Portable', size=128, required=False, readonly=False)
    email = fields.Char('email', size=128, required=False, readonly=False)
    employee_id = fields.Many2one('hr.employee', 'Employé', required=False)


class personne_contacted(models.Model):
    _name = 'hr.personne.contacted'
    _description = 'Personnes a contacter'

    name = fields.Char("Name", size=128, required=True)
    email = fields.Char("Email", size=128)
    portable = fields.Char('Portable', size=128, required=True)
    state = fields.Selection([('grand_parent', 'Grand père/Grande mère'), ('parent', 'Père / Mère'),
                              ('conjoint', 'Conjoint(e)'), ('enfant', 'Enfant'), ('frere', 'Frère / Soeur'),
                              ('voisin', 'Voisin'),
                              ('oncle', 'Oncle/Tante'), ('cousin', 'Cousin / Cousine'), ('other', 'Autres')],
                             'Type de lien', readonly=False)
    Lien = fields.Char("Le lien", size=128)
    employee_id = fields.Many2one("hr.employee", 'Employé')


class HrEmployee(models.Model):
    _inherit = 'hr.employee'
    # _rec_name = 'identification_id'

    #@api.depends('total_children')
    def _get_part_igr(self):
        result = 0
        for rec in self:
            if rec.marital:
                t1 =rec.marital
                B38 = t1[0]
                B39 = rec.children
                B40 = rec.enfants_a_charge

                if ((B38 == "s") or (B38 == "d")):
                    if (B39 == 0):
                        if (B40 != 0):
                            result = 1.5
                        else:
                            result = 1
                    else:
                        if ((1.5 +  B39 * 0.5) > 5):
                            result = 5
                        else:
                            result = 1.5 + B39 * 0.5
                else:
                    if (B38 == "m"):
                        if (B39 == 0):
                            result = 2
                        else:
                            if ((2 + 0.5 * B39) > 5):
                                result = 5
                            else:
                                result = 2 + 0.5 * B39
                    else:
                        if (B38 == "w"):
                            if (B39 == 0):
                                if (B40 != 0):
                                    result = 1.5
                                else:
                                    result = 1
                            else:
                                if ((2 + B39 * 0.5) > 5):
                                    result = 5
                                else:
                                    result = 2 + 0.5 * B39
                        else:
                            result += 2 + 0.5 * B39
            rec.part_igr = result
    # def _get_part_igr(self):
    #     for rec in self:
    #         result = 0
    #         if rec.marital:
    #             t1 = rec.marital
    #             B38 = t1[0]
    #             B39 = rec.children
    #             # B40 = rec.total_children
    #
    #             if (B38 == "s") or (B38 == "d"):
    #                 if B39 <= 5:
    #                     result = 1 + B39 * 0.5
    #                 else:
    #                     result = 1 + 5 * 0.5
    #             else:
    #                 if B38 == "m":
    #                     if B39 == 0:
    #                         result = 2
    #                     else:
    #                         if B39 > 5:
    #                             result = 2 + 5 * 0.5
    #                         else:
    #                             result = 2 + B39 * 0.5
    #                 else:
    #                     if B38 == "w":
    #                         if B39 == 0:
    #                             result = 2
    #                         else:
    #                             if B39 <= 5:
    #                                 result = 2 + B39 * 0.5
    #                             else:
    #                                 result = 2 + 5 * 0.5
    #         rec.part_igr = result

    @api.depends('enfants_ids', 'enfants_a_charge')
    def _compute_children(self):
        children_in_charge = 0
        for emp in self:
            for child in emp.enfants_ids:
                if child.age <= emp.company_id.max_age_child:
                    children_in_charge += 1
            emp.children = children_in_charge
            emp.total_children = emp.children + emp.enfants_a_charge
            children_in_charge = 0

    @api.depends('birthday')
    def _get_age_employee(self):
        this_date = fields.Datetime.now()
        for emp in self:
            date_naissance = fields.Datetime.from_string(emp.birthday)
            tmp = relativedelta(this_date, date_naissance)
            emp.age = tmp.years

    @api.depends('start_date', 'end_date')
    def _get_seniority(self):
        today = fields.Datetime.now()

        for emp in self:
            start_date = fields.Datetime.from_string(emp.start_date)
            if emp.end_date:
                end_date = fields.Datetime.from_string(emp.end_date)
                this_date = min(today, end_date)
            else:
                this_date = today
            tmp = relativedelta(this_date, start_date)
            emp.seniority_employee = tmp.years

    def _get_nb_part_cmu(self):
        for emp in self:
            nb = emp.children + 1
            if emp.marital == "married":
                nb += 1
            emp.part_cmu = nb

    identification_id = fields.Char('Matricule')
    first_name = fields.Char("Prénoms")
    category_id = fields.Many2one('hr.contract.category', 'Catégorie', required=False)
    type = fields.Selection(Type_employee, 'Type', required=False, default=False)
    matricule_cnps = fields.Char('N° CNPS', size=64)
    enfants_a_charge = fields.Integer("Nombre d'enfants à charge", required=True, default=0)
    part_igr = fields.Float(compute=_get_part_igr, string='Part IGR')
    start_date = fields.Date("Date d'ancièneté")
    seniority_employee = fields.Integer("Anciennété", compute="_get_seniority")
    end_date = fields.Date("Date de depart", required=False)
    age = fields.Integer('Âge employé', compute='_get_age_employee')
    total_children = fields.Integer('Nombre enfant total a charge', compute=_compute_children, store=True)
    enfants_ids = fields.One2many('hr.employee.enfant', 'employee_id', 'Enfants', required=False)
    licence_ids = fields.One2many('hr.licence', 'employee_id', 'Licences des employés')
    diplome_ids = fields.One2many('hr.diplomes.employee', 'employee_id', 'Diplôme des employés')
    visa_ids = fields.One2many('hr.visa', 'employee_id', 'Visas des employés')
    carte_sejour_ids = fields.One2many('hr.carte.sejour', 'employee_id', 'Carte de séjour des employés')
    children = fields.Integer("Nombre d'enfant", compute=_compute_children, store=True)
    date_entree = fields.Date("Date d'entrée")
    # piece_identite_id = fields.Many2one("hr.piece.identite", "Pièce d'identité")
    presonnes_contacted_ids = fields.One2many('hr.personne.contacted', 'employee_id', 'Personnes à contacter')
    parent_employee_ids = fields.One2many("hr.parent.employe", 'employee_id', 'Les parents')
    recruitment_degree_id = fields.Many2one('hr.employee.degree', "Niveau d'étude")
    #direction_id = fields.Many2one('hr.department', 'Direction', required=False, domain="[('type', '=', 'direction')]")
    direction_id = fields.Many2one('hr.department', 'Direction', required=False)
    #department_id = fields.Many2one('hr.department', 'Departement', required=False, domain="[('type', '=', 'department')]")
    department_id = fields.Many2one('hr.department', 'Departement', required=False)
    #service_id = fields.Many2one('hr.department', 'Service', domain="[('type', '=', 'service')]")
    service_id = fields.Many2one('hr.department', 'Service')
    conjoint_name = fields.Char(string="Nom conjoint(e)", groups="hr.group_hr_user")
    conjoint_first_name = fields.Char(string="Prénoms conjoint(e)", groups="hr.group_hr_user")
    conjoint_birthdate = fields.Date(string="Date de naissance du conjoint", groups="hr.group_hr_user")
    gender_conjoint = fields.Selection([('male', 'M'), ('female', 'F')], "Sexe", groups="hr.group_hr_user")
    nature_employe = fields.Selection([('local', 'Local'), ('expat', 'Expatrié')], "Nature de l'employé",
                                      default='local')
    num_cmu_conjoint = fields.Char('N° CMU conjoint', required=False)
    part_cmu = fields.Integer("Nombre de part CMU", compute="_get_nb_part_cmu")
    qualification_id = fields.Many2one("hr.payroll.ci.qualification", "Qualification")
    study_level_id = fields.Many2one('hr_update.study_level','Niveau etude')

    # def name_get(self):
    #     """
    #     Change the way an employee's name that displayed for migrate data
    #     :return:
    #     """
    #     reads = self.read(['name_related', 'identification_id'])
    #     res = []
    #     for record in reads:
    #         if record['identification_id']:
    #             name = record['identification_id']
    #         res.append((record['id'], name))
    #     return res


class HrQualification(models.Model):
    _name = "hr.payroll.ci.qualification"
    _description = "Employee qualification"

    name = fields.Char("Libellé")


class HrStudyLevel(models.Model):
    _name = 'hr_update.study_level'
    _description = "Niveau etudes"

    name = fields.Char('Niveau etude')

