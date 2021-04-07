# -*- coding:utf-8 -*-

from odoo import api, fields, models, _
from dateutil import relativedelta


class HrAgence(models.Model):
    _name = 'hr.agence'
    _description = "hr agence"

    name = fields.Char('Libellé', required=True)
    description = fields.Text('Description')


class VisiteMedical(models.Model):
    _name = 'hr.visit.medical'
    _description = "Gestion des visites medicals"

    name = fields.Char('Libellé', required=True)
    date_prevue = fields.Date("Date prévue", required=True)
    date_effective = fields.Date("Date éffective", required=True)
    description = fields.Text("Commentaire")
    lieu_visite = fields.Char("Lieu de la visite", required=True)
    employee_id = fields.Many2one('hr.employee', "Employé", required=False)


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    @api.depends("date_return_last_holidays", "start_date")
    def _get_estimed_holidays(self):
        today = fields.Datetime.now()
        for emp in self:
            facteur = emp.company_id.number_holidays_locaux if emp.nature_employe == 'local' \
                else emp.company_id.number_holidays_expat
            emp.date_return_last_holidays = False
            if emp.date_return_last_holidays:
                start = fields.Date.from_string(emp.date_return_last_holidays)
                vals = {
                    'estimed_date_leave': False,
                    'number_days_estimed_holidays': 0,
                    'estimated_date_return_leave': False
                }
                if emp.date_return_last_holidays == emp.start_date and emp.seniority_employee >= 1:
                    vals['estimed_date_leave'] = fields.Date.from_string(emp.start_date) + \
                                                 relativedelta.relativedelta(year=today.year)
                else:
                    vals['estimed_date_leave'] = fields.Date.from_string(emp.date_return_last_holidays) + \
                                                 relativedelta.relativedelta(years=+1)
                tmp = vals['estimed_date_leave'] - start
                vals['number_days_estimed_holidays'] = tmp.days * 12 / 360 * facteur
                vals['estimated_date_return_leave'] = vals['estimed_date_leave'] + relativedelta.relativedelta(
                    days=+vals['number_days_estimed_holidays'])
                emp.update(vals)

    def name_get(self):
        result = []
        for emp in self:
            if emp.first_name:
                name = emp.name + ' ' + emp.first_name
            else:
                name = emp.name
            result.append((emp.id, name))
        return result

    medic_exam = fields.Date(string='Medical Examination Date', groups="hr.group_hr_user")
    bank_ids = fields.One2many("res.partner.bank", "employee_id", "Comptes bancaires")
    main_bank_id = fields.Many2one("res.partner.bank", "Compte bancaire principale",
                                   domain="[('employee_id', '=', id)]")
    dispatch_bank_ids = fields.One2many('hr.employee.salary.dispatched.line', 'employee_id', 'Repartition du salaire')
    motif_fin_contract_id = fields.Many2one('hr.employee.motif.cloture', "Motif de fin", required=False)
    motif_depart = fields.Text('Commentaire de depart')
    college = fields.Selection([('cadre', 'Cadre'), ('non_cadre', 'Non cadre')], string="Collège", default=False)
    agence_id = fields.Many2one('hr.agence', 'Agence', required=False)
    type_employee = fields.Selection([('director', 'Directeur'), ('department_chief', 'Chef de departement'),
                                      ('service_chief', 'chef de service'), ('employee', 'Collaborateur'),
                                      ('general_director', 'Directeur général'), ('project_manager', 'Chef de projet')],
                                     "Type de l'employé")
    current_leave_state = fields.Selection(
        selection_add=[('direction', 'Directeur'), ('department', 'Chef de departement'),
                       ('service', 'Chef de service')])
    date_first_alerte_retraite = fields.Date("Date première alerte retraite")
    date_second_alerte_retraite = fields.Date("Date seconde alerte retraite")
    medic_exam_yearly = fields.Date("Visite médicale annuelle", required=False)
    date_annienete = fields.Date("Date d'embauche", required=False)
    # type_piece_id = fields.Many2one('hr.employee.nature_piece', "Type de pièce", required=False)
    # num_piece = fields.Char("Numéro de la pièce", required=False)
    mobile_personnal = fields.Char("Tél Portable personnel")
    gender = fields.Selection([
        ('male', 'M'),
        ('female', 'F'),
        ('other', 'Autre')
    ], groups="hr.group_hr_user", default="male")
    visit_ids = fields.One2many('hr.visit.medical', 'employee_id', "Visistes médicales")
    email_personal = fields.Char("Email personnel", required=False)
    estimed_date_leave = fields.Date("Date prévisonnelle de depart en congés", compute="_get_estimed_holidays",
                                     store=True)
    number_days_estimed_holidays = fields.Integer("Nombre de jours de congés estimés", compute="_get_estimed_holidays",
                                                  store=True)
    estimated_date_return_leave = fields.Date("Date prévisonnelle de retour en congés", compute="_get_estimed_holidays",
                                              store=True)
    num_cgare = fields.Char("N° CGRAE", required=False)
    num_crrae = fields.Char('N° CRRAE', required=False)
    num_cmu = fields.Char('N° CMU', required=False)
    first_name = fields.Char("Prenoms", required=True)

    @api.onchange('end_date')
    @api.depends('end_date')
    def onChangeDateEnd(self):
        if self.company_id and self.end_date:
            first_date = str(fields.Date.from_string(self.end_date) + relativedelta.relativedelta(
                months=- self.company_id.first_alert_retraite))
            second_date = str(fields.Date.from_string(self.end_date) + relativedelta.relativedelta(
                months=- self.company_id.second_alert_retraite))
            self.date_first_alerte_retraite = first_date
            self.date_second_alerte_retraite = second_date

    @api.depends("enfants_ids")
    def _compute_children(self):
        for emp in self:
            emp.total_children = len(emp.enfants_ids)
            children_in_charge = 0
            for child in emp.enfants_ids:
                if child.age <= emp.company_id.max_age_child:
                    children_in_charge += 1
                else:
                    if child.certification_frequentation:
                        children_in_charge += 1
            emp.children = children_in_charge


class Department(models.Model):
    _inherit = "hr.department"
    _rec_name = 'name'


class ChildEmployee(models.Model):
    _inherit = "hr.employee.enfant"

    @api.model
    def send_notifcation_certification(self):
        today = fields.Date.from_string(fields.Date.today())

        enfants = self.search([])

        for eft in enfants:
            if eft.age >= 21:
                # TODO: send notification
                return True
            values = {}

    certification_frequentation = fields.Boolean("Certificat de frequentation")
    num_cmu = fields.Char('N° CMU', required=False)


class HrEmployeeMotifCloture(models.Model):
    _name = 'hr.employee.motif.cloture'
    _description = "hr employe motif cloture"

    name = fields.Char('Libellé', required=True)
    description = fields.Text('Description', required=False)

#
# class HrEmployeeNaturePiece(models.Model):
#     _name = "hr.employee.nature_piece"
#     _description = "Nature de la piece"
#
#     name = fields.Char("Libellé", required=True, size=225)
#     description = fields.Text("Description", required=False)
