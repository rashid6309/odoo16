from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalGynaecologicalExamination(models.Model):
    _name = "ec.medical.gynaecological.examination"
    _description = "Patient Gynaecological Examination"

    consultation_id = fields.Many2one(comodel_name='ec.first.consultation', string='First Consultation')

    vulva_vagina = fields.Selection(selection=StaticMember.UTERUS_SIZE, string='Vulva/Vagina')
    vulva_vagina_comment = fields.Char(string='Vulva/Vagina')

    uterus_size = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='Uterus Size')
    uterus_size_comment = fields.Char(string='Uterus Size')

    uterus_position = fields.Selection(selection=StaticMember.UTERUS_POSITION, string='Uterus Position')
    uterus_mobility = fields.Selection(selection=StaticMember.UTERUS_MOBILITY, string='Uterus Mobility')

    gynaecological_examination_ps_selection = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='PS')
    gynaecological_examination_ps_comment = fields.Char('PS')

    gynaecological_examination_date = fields.Date(string='Date')

    gynaecological_examination_lmp = fields.Date(string='LMP')

    gynaecological_examination_comment = fields.Char('Comments')

    # LEFT OVARY FIELDS

    left_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    '''
        FIXME: What is length and width?
        Need to move to One2Many relation based on the left and right ovary. this is not required
    '''
    left_ovary_length_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_width_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_length_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_width_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_length_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_width_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_length_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_width_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_length_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_width_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')

    # Right OVARY FIELDS

    '''
        FIXME: What is length and width?

    '''

    right_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_length_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_width_1 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_length_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_width_2 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_length_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_width_3 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_length_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_width_4 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_length_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_width_5 = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')

    uterus = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')
    uterus_size_length = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')
    uterus_size_width = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')

    uterus_size_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION, string='Uterus')
    uterus_nos = fields.Selection(selection=StaticMember.UTERUS_NOS, string='Nos')

    forbid_size_length_1 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_1 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')

    forbid_size_length_2 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_2 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_3 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_3 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_4 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_4 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_5 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_5 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_6 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_6 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_7 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_7 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_8 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_8 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_9 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_9 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_length_10 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')
    forbid_size_width_10 = fields.Selection(selection=StaticMember.FORBID, string='Forbid')

    lining = fields.Selection(selection=StaticMember.LINING, string='Lining')
    lining_size = fields.Selection(selection=StaticMember.LINING_SIZE, string='Lining')

