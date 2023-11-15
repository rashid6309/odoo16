from odoo import api, models, fields, _
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class EcContraception(models.Model):
    _name = 'ec.sx.contraception'
    _description = "Patient Contraception"

    sx_frequency = fields.Selection(selection=StaticMember.YEARS,
                                    string="Frequency")
    sx_issues = fields.Selection(selection=StaticMember.SX_ISSUES,
                                 string="Issues")

    sx_comments = fields.Text(string="Comments")

    # cn_type = fields.Selection(selection=StaticMember.CN_TYPES,
    #                            string="Type")

    cn_type = fields.Many2many(comodel_name='ec.medical.multi.selection',
                               relation='contraception_multi_selection_cn_type',
                               column1='contraception_id',
                               column2='multi_selection_id',
                               string='Type',
                               domain="[('type', '=', 'cn_type')]")

    other_comments = fields.Text(string="Comments")

    ''' Male attributes '''

    male_sx_performance = fields.Selection(selection=StaticMember.SX_PERFORMANCE,
                                           string="Performance")

    male_other = fields.Text(string="Other")
