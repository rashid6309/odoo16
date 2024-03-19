from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class MedicalGynaecologicalExamination(models.Model):
    _name = "ec.medical.gynaecological.examination"
    _description = "Patient Gynaecological Examination"

    gynaecological_examination_patient_id = fields.Many2one(comodel_name="ec.medical.patient", ondelete='restrict')

    consultation_id = fields.Many2one(comodel_name='ec.first.consultation', string='First Consultation')

    vulva_vagina = fields.Selection(selection=StaticMember.UTERUS_SIZE, string='Vulva/Vagina')
    vulva_vagina_comment = fields.Char(string='Vulva/Vagina Comment')

    uterus_size = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='Uterus Size')
    uterus_size_comment = fields.Char(string='Uterus Size Comment')

    uterus_flexion = fields.Selection(selection=StaticMember.UTERUS_FLEXION,
                                      string="Uterus Flexion")

    uterus_position = fields.Selection(selection=StaticMember.UTERUS_POSITION, string='Uterus Position')
    # TODO Field name needed to be refactored as well
    uterus_motility = fields.Selection(selection=StaticMember.UTERUS_MOTILITY, string='Uterus Mobility')

    gynaecological_examination_ps_selection = fields.Selection(selection=StaticMember.ORGAN_SIZE,  string='P/S')
    gynaecological_examination_ps_comment = fields.Char('P/S Comment')

    # Fields for gynae_exam
    gynae_exam_pelvic_examination_state = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                           string="Pelvic examination done?")
    gynae_exam_inspection_only = fields.Boolean(string='Inspection Only')
    gynae_exam_p_v_only = fields.Boolean(string='P/V Only')
    gynae_exam_p_s_only = fields.Boolean(string='P/S Only')

    gynae_exam_findings_on_inspection = fields.Text(string='Findings on Inspection')
    gynae_exam_valva_vaginal_exam = fields.Text(string='Vulva Vaginal Exam')
    gynae_exam_cervix = fields.Text(string='Cervix')
    gynae_exam_uterus_and_adnexae = fields.Text(string='Uterus and adnexae (bimanual)')

    gynae_exam_hvs = fields.Boolean(string='HVS')
    gynae_exam_endocervical = fields.Boolean(string='Endocervical')
    gynae_exam_no_swab_taken = fields.Boolean(string="No swab taken")
    gynae_exam_method_of_hvs = fields.Selection(string="Method of HVS",
                                                selection=StaticMember.METHOD_OF_HVS)

    gynae_exam_pap_smear_done = fields.Boolean(string='Pap Smear Done')
    gynae_exam_pipelle_sampling_done = fields.Boolean(string='Pipelle Sampling Done')

    gynae_exam_other_findings = fields.Text(string='Other Findings')

    gynaecological_examination_date = fields.Date(string='Date')
    gynaecological_ultrasound_type = fields.Selection(selection=StaticMember.ULTRASOUND_TYPE,
                                                      string="Ultrasound")

    gynaecological_examination_lmp = fields.Date(string='LMP')

    gynaecological_examination_comment = fields.Char('Comments')

    # LEFT OVARY FIELDS

    left_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary')
    left_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE_TYPE, string='Left Ovary Type')
    gynaecological_left_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                                   inverse_name="gynaecological_left_size_id",
                                                   string="Left Ovary")
    left_ovary_not_visualised = fields.Boolean(string='Not Visualised', default=False)
    gynae_uterus_flexion = fields.Selection(selection=StaticMember.UTERUS_FLEXION, string='Uterus Flexion')
    left_ovary_nos = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Left Ovary Nos')
    '''
        FIXME: What is length and width?
        Need to move to One2Many relation based on the left and right ovary. this is not required
    '''

    # Right OVARY FIELDS

    '''
        FIXME: What is length and width?

    '''

    gynae_cyst_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                          inverse_name="gynaecological_fiobrid_id",
                                          string="Fibroid")
    gynae_rov = fields.Char(string='ROV')

    gynae_lov = fields.Char(string='LOV')
    right_ovary = fields.Selection(selection=StaticMember.OVARY_SIZE, string='Right Ovary')
    right_ovary_type = fields.Selection(selection=StaticMember.OVARY_SIZE_TYPE, string='Right Ovary Type')
    gynaecological_right_size_ids = fields.One2many(comodel_name="ec.generic.size",
                                                    inverse_name="gynaecological_right_size_id",
                                                    string="Right Ovary")
    right_ovary_not_visualised = fields.Boolean(string='Not Visualised', default=False)

    uterus = fields.Selection(selection=StaticMember.UTERUS_TYPE_SIZE, string='Uterus')

    gynaecological_uterus_size = fields.Boolean(default=False, string="Size")
    gynaecological_uterus_position = fields.Boolean(default=False, string="Position")
    # gynaecological_uterus_normal = fields.Boolean(default=False, string="Normal")
    gynaecological_uterus_fiobrid = fields.Boolean(default=False, string="Fibroid")

    uterus_size_length = fields.Selection(selection=StaticMember.SIZE_INTEGER, string='Uterus Length')
    uterus_size_width = fields.Selection(selection=StaticMember.SIZE_INTEGER, string='Uterus Width')

    uterus_size_position = fields.Selection(selection=StaticMember.UTERUS_SIZE_POSITION, string='Uterus Position')
    
    gynae_position_to_left = fields.Boolean(string="Deviated to Left", default=False)
    gynae_position_to_right = fields.Boolean(string="Deviated to Right", default=False)
    gynae_position_a_v = fields.Boolean(string="A/V", default=False)
    gynae_position_r_v = fields.Boolean(string="R/V", default=False)
    gynae_position_mid_position = fields.Boolean(string="Mid Position", default=False)


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
                                  string='Endometrial Lining Character', domain="[('type', '=', 'linining')]")

    gynae_smooth = fields.Boolean(string="Smooth", default=False)
    gynae_distorted = fields.Boolean(string="Distorted", default=False)
    gynae_triple_echo = fields.Boolean(string="Triple Echo", default=False)
    gynae_hyperechoic_solid = fields.Boolean(string="Hyperechoic/Solid", default=False)
    gynae_suspected_cavity_lesion = fields.Boolean(string="Suspected Cavity Lesion", default=False)

    lining_size = fields.Selection(selection=StaticMember.SIZE_INTEGER, string='CET')

    def action_open_gynae_scan(self):
        context = self._context.copy()
        if context:
            field = context.get('default_field')
            if field:
                return {
                    "name": _("TVS Scan"),
                    "type": 'ir.actions.act_window',
                    "res_model": 'ec.medical.tvs.scan',
                    'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_scan_form').id,
                    'view_mode': 'form',
                    "target": 'new',
                    "context": {
                        'default_gynae_id': self.id,
                        'default_field': field
                    },
                }
