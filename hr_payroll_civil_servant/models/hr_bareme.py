# -*- coding:utf-8 -*-


from odoo import api, fields, models, _


class HrBaremeFonctionnaire(models.Model):
    _name = "hr.bareme.fonctionnaire"
    _description = "Bareme fonctionnaire"


    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")


class HrClasseFonctionnaire(models.Model):
    _name = "hr.classe.fonctionnaire"
    _description = "Classe de fonctionnaire"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")


class HrEchelonFonctionnaire(models.Model):
    _name = "hr.echelon.fonctionnaire"
    _description = "Echelon des fonctionnaires"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")


class HrCategoryFonctionnaire(models.Model):
    _name = "hr.category.fonctionnaire"
    _description = "Cetgorie fonctionnaire"

    name = fields.Char("Libellé", required=True)
    description = fields.Text("Description")


class HrCategoryFonctionnaireLine(models.Model):
    _name = "hr.category.fonctionnaire.line"
    _description = "Category fonctionnaire line"

    name = fields.Char("Libellé", required=True)
    bareme = fields.Float("Barème", default=0)
    category_id = fields.Many2one("hr.category.fonctionnaire", "Catégorie", required=False)
