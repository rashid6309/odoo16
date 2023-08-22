from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcContraception(models.Model):
    _name = 'ec.sx.contraception'
    _description = "Patient Contraception"

    sx_frequency = fields.Integer(string="Frequency")
    sx_issues = fields.Selection(selection=StaticMember.SX_ISSUES,
                                 string="Issues")

    sx_comments = fields.Char(string="Comments")

    cn_type = fields.Selection(selection=StaticMember.CN_TYPES,
                               string="Type")

    other_comments = fields.Char(string="Other")

    ''' Male attributes '''

    male_sx_performance = fields.Selection(selection=StaticMember.SX_PERFORMANCE,
                                           string="Performance")

    male_other = fields.Char(string="Other")


