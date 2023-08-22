from odoo import models, fields
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GenitalExamination(models.Model):
    _name = "ec.genital.examination"
    _description = "Genital Examination"
    _rec_name = 'skin_condition'

    ''' Data-members '''
    skin_condition = fields.Char(string="Skin Condition")

    # SIDES
    hernia = fields.Selection(selection=StaticMember.SIDE, )
    vericocele = fields.Selection(selection=StaticMember.SIDE, )
    hydrocele = fields.Selection(selection=StaticMember.SIDE, )
    undescended_testis = fields.Selection(selection=StaticMember.SIDE, )
    supermatic_cord_normal = fields.Selection(selection=StaticMember.SIDE, )
    supermatic_cord_thick = fields.Selection(selection=StaticMember.SIDE, )
    supermatic_cord_tender = fields.Selection(selection=StaticMember.SIDE, )

    testicular_size_right = fields.Selection(selection=StaticMember.SIZE, )
    testicular_size_left = fields.Selection(selection=StaticMember.SIZE, )

    testicular_size_mobility = fields.Selection(selection=StaticMember.CHOICE_YES_NO, )
    comment = fields.Char(string="Comment")



