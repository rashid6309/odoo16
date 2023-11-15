from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalGynaecologicalExamination(models.Model):
    _name = "ec.medical.gynaecological.examination"
    _description = "Patient Gynaecological Examination"

    consultation_id = fields.Many2one(comodel_name='ec.first.consultation', string='First Consultation')

    vulva_vagina = fields.Selection(selection=StaticMember.UTERUS_SIZE, string='Vulva/Vagina')
    vulva_vagina_comment = fields.Char(string='Vulva/Vagina Comment')

    uterus_size = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='Uterus Size')
    uterus_size_comment = fields.Char(string='Uterus Size Comment')

    uterus_position = fields.Selection(selection=StaticMember.UTERUS_POSITION, string='Uterus Position')
    uterus_mobility = fields.Selection(selection=StaticMember.UTERUS_MOBILITY, string='Uterus Mobility')

    gynaecological_examination_ps_selection = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='P/S')
    gynaecological_examination_ps_comment = fields.Char('P/S Comment')

    gynaecological_examination_date = fields.Date(string='Date')

    gynaecological_examination_lmp = fields.Date(string='LMP')

    gynaecological_examination_comment = fields.Char('Comments')

    # LEFT OVARY FIELDS

    left_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Type')
    gynaecological_left_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                                   inverse_name="gynaecological_left_size_id",
                                                   string="Left Ovary")

    left_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Nos')
    '''
        FIXME: What is length and width?
        Need to move to One2Many relation based on the left and right ovary. this is not required
    '''

    # Right OVARY FIELDS

    '''
        FIXME: What is length and width?

    '''
    right_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Type')
    gynaecological_right_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                                    inverse_name="gynaecological_right_size_id",
                                                    string="Right Ovary")


    uterus = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')

    gynaecological_uterus_size = fields.Boolean(default=False, string="Size")
    gynaecological_uterus_position = fields.Boolean(default=False, string="Position")
    gynaecological_uterus_normal = fields.Boolean(default=False, string="Normal")
    gynaecological_uterus_fiobrid = fields.Boolean(default=False, string="Fibroid")

    uterus_size_length = fields.Selection(selection=StaticMember.SIZE_INTEGER, string='Uterus Length')
    uterus_size_width = fields.Selection(selection=StaticMember.SIZE_INTEGER, string='Uterus Width')

    uterus_size_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION, string='Uterus Position')

    gynaecological_uterus_position_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                                          relation='gynaecological_uterus_multi_selection_repeat_position',
                                                          column1='gynaecological_id',
                                                          column2='multi_selection_id',
                                                          string='Position',
                                                          domain="[('type', '=', 'position')]")

    uterus_nos = fields.Selection(selection=StaticMember.UTERUS_NOS, string='Nos')

    gynaecological_generic_sizes_ids = fields.One2many(comodel_name="ec.generic.size",
                                                       inverse_name="gynaecological_fiobrid_id",
                                                       string="Sizes")


    lining_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                  relation='gynaecological_examination_multi_selection_lining',
                                  column1='gynaecological_id',
                                  column2='multi_selection_id',
                                  string='Lining', domain="[('type', '=', 'linining')]")
    lining_size = fields.Selection(selection=StaticMember.LINING_SIZE, string='Lining Size')

