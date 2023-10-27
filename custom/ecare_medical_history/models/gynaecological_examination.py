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
    left_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Nos')
    '''
        FIXME: What is length and width?
        Need to move to One2Many relation based on the left and right ovary. this is not required
    '''
    left_ovary_length_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Length 1')
    left_ovary_width_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Width 1')
    left_ovary_length_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Length 2')
    left_ovary_width_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Width 2')
    left_ovary_length_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Length 3')
    left_ovary_width_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Width 3')
    left_ovary_length_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Length 4')
    left_ovary_width_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Width 4')
    left_ovary_length_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Length 5')
    left_ovary_width_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Width 5')

    # Right OVARY FIELDS

    '''
        FIXME: What is length and width?

    '''
    right_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Type')
    right_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Nos')
    right_ovary_length_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Length 1')
    right_ovary_width_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Width 1')
    right_ovary_length_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Length 2')
    right_ovary_width_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Width 2')
    right_ovary_length_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Length 3')
    right_ovary_width_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Width 3')
    right_ovary_length_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Length 4')
    right_ovary_width_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Width 4')
    right_ovary_length_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Length 5')
    right_ovary_width_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary Width 5')

    uterus = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')
    uterus_size_length = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus Length')
    uterus_size_width = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus Width')

    uterus_size_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION, string='Uterus Position')
    uterus_nos = fields.Selection(selection=StaticMember.UTERUS_NOS, string='Nos')

    forbid_size_length_1 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 1')
    forbid_size_width_1 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 1')

    forbid_size_length_2 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 2')
    forbid_size_width_2 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 2')
    forbid_size_length_3 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 3')
    forbid_size_width_3 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 3')
    forbid_size_length_4 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 4')
    forbid_size_width_4 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 4')
    forbid_size_length_5 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 5')
    forbid_size_width_5 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 5')
    forbid_size_length_6 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 6')
    forbid_size_width_6 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 6')
    forbid_size_length_7 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 7')
    forbid_size_width_7 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 7')
    forbid_size_length_8 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 8')
    forbid_size_width_8 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 8')
    forbid_size_length_9 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 9')
    forbid_size_width_9 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 9')
    forbid_size_length_10 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Length 10')
    forbid_size_width_10 = fields.Selection(selection=StaticMember.FORBID, string='Forbid Width 10')

    lining_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                  relation='gynaecological_examination_multi_selection_lining',
                                  column1='gynaecological_id',
                                  column2='multi_selection_id',
                                  string='Lining', domain="[('type', '=', 'linining')]")
    lining_size = fields.Selection(selection=StaticMember.LINING_SIZE, string='Lining Size')

