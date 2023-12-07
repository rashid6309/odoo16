from odoo import models, fields
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class GenitalExamination(models.Model):
    _name = "ec.genital.examination"
    _description = "Genital Examination"
    _rec_name = 'skin_condition'

    ''' Data-members '''
    skin_condition = fields.Char(string="Skin Condition")

    # SIDES
    # hernia = fields.Selection(selection=StaticMember.SIDE, )
    # vericocele = fields.Selection(selection=StaticMember.SIDE, )
    # hydrocele = fields.Selection(selection=StaticMember.SIDE, )
    # undescended_testis = fields.Selection(selection=StaticMember.SIDE, )
    # supermatic_cord_normal = fields.Selection(selection=StaticMember.SIDE, )
    # supermatic_cord_thick = fields.Selection(selection=StaticMember.SIDE, )
    # supermatic_cord_tender = fields.Selection(selection=StaticMember.SIDE, )

    testicular_size_right = fields.Selection(selection=StaticMember.SIZE, )
    testicular_size_left = fields.Selection(selection=StaticMember.SIZE, )

    testicular_size_motility = fields.Selection(selection=StaticMember.CHOICE_YES_NO, )

    ec_genital_examination_comment = fields.Char(string="Comment")

    hernia_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                  relation='genital_examination_multi_selection_hernia',
                                  column1='genital_examination_id',
                                  column2='multi_selection_id',
                                  string='Hernia', domain="[('type', '=', 'hernia')]")

    vericocele_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                      relation='genital_examination_multi_selection_vericocele',
                                      column1='genital_examination_id',
                                      column2='multi_selection_id',
                                      string='Vericocele', domain="[('type', '=', 'vericocele')]")

    hydrocele_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                     relation='genital_examination_multi_selection_hydrocele',
                                     column1='genital_examination_id',
                                     column2='multi_selection_id',
                                     string='Hydrocele', domain="[('type', '=', 'hydrocele')]")

    undescended_testis_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                  relation='genital_examination_multi_selection_undescended_testis',
                                                  column1='genital_examination_id',
                                                  column2='multi_selection_id',
                                                  string='Undescended Testis',
                                                  domain="[('type', '=', 'undescended_testis')]")

    supermatic_cord_normal_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                  relation='genital_examination_multi_selection_supermatic_cord_normal',
                                                  column1='genital_examination_id',
                                                  column2='multi_selection_id',
                                                  string='Spermatic Cord Normal', domain="[('type', '=', 'supermatic_cord_normal')]")

    supermatic_cord_thick_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                 relation='genital_examination_multi_selection_supermatic_cord_thick',
                                                 column1='genital_examination_id',
                                                 column2='multi_selection_id',
                                                 string='Spermatic Cord Thick', domain="[('type', '=', 'supermatic_cord_thick')]")

    supermatic_cord_tender_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                  relation='genital_examination_multi_selection_supermatic_cord_tender',
                                                  column1='genital_examination_id',
                                                  column2='multi_selection_id',
                                                  string='Spermatic Cord Tender', domain="[('type', '=', 'supermatic_cord_tender')]")
