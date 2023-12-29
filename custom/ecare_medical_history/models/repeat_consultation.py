from odoo import api, models, fields, _
from odoo.exceptions import UserError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from logging import getLogger

_logger = getLogger(__name__)


class RepeatConsultation(models.Model):
    _name = 'ec.repeat.consultation'
    _description = "Patient Repeat Consultation"
    _order = "create_date desc"
    _inherits = {
        'ec.medical.tvs': 'repeat_tvs_id',
        'ec.medical.pregnancy.data': 'repeat_pregnancy_id',
        'female.ot.ti.checklist': 'female_ot_ti_checklist_id',
        'male.ot.ti.checklist': 'male_ot_ti_checklist_id',
        'medical.consents.risk.assessment': 'medical_consents_risk_assessment_id',
    }

    ''' Foreign Keys '''

    repeat_patient_id = fields.Many2one(comodel_name="ec.medical.patient")
    repeat_timeline_id = fields.Many2one(comodel_name="ec.patient.timeline", ondelete="restrict")

    repeat_tvs_id = fields.Many2one(comodel_name="ec.medical.tvs")
    repeat_pregnancy_id = fields.Many2one(comodel_name="ec.medical.pregnancy.data")
    female_ot_ti_checklist_id = fields.Many2one(comodel_name="female.ot.ti.checklist",
                                                ondelete='restrict')
    male_ot_ti_checklist_id = fields.Many2one(comodel_name="male.ot.ti.checklist",
                                              ondelete='restrict')
    medical_consents_risk_assessment_id = fields.Many2one(comodel_name="medical.consents.risk.assessment",
                                                          ondelete='restrict')


    ''' Data attributes '''
    #
    # repeat_state = fields.Selection(selection=[('1', "Question 1"),
    #                                            ('2', "Question 2"),
    #                                            ('3', "Question 3"),
    #                                            ('4', "Question 4")],
    #                                 default="1",
    #                                 required=True)
    first_consultation_state = fields.Selection([('open', 'In Progress'),
                                                 ('closed', 'Done'),
                                                 ('decision_pending', "Decision Pending"),
                                                 ],
                                                default='open',
                                                string='State')

    """ Question One
    Yes: Open the pregnancy assessment form
        * LMP (Added manually)
        * LMP for Embryo
    No: move to the next question
    """

    question_one_label = fields.Char(string="Question 1:",
                                     default="Is the couple currently pregnant?",
                                     store=False,
                                     readonly=1,
                                     )
    question_one_choice = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                           string="Choice",
                                           default='no')

    repeat_lmp = fields.Date(string="LMP",
                             readonly=True,
                             )
    repeat_lmp_embryo = fields.Date(string="LMP Embryo",
                                    readonly=True,
                                    )

    """ Question Two
        Yes: Move to obstetrics 
        No: Move to next
    """
    question_two_label = fields.Char(string="Question 2:",
                                     default="Has the couple had any conception since the last visit?",
                                     store=False,
                                     readonly=True)
    question_two_choice = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                           string="Choice",
                                           default='no')

    """ Question Three
        Yes: Open the treatment outside of ICSI from and add a record in the previous treatment history 
        No: move to next question

    """
    question_three_label = fields.Char(string="Question 3:",
                                       default="Has the couple had any treatment outside of ICSI Pvt. Ltd. since last visit?",
                                       store=False,
                                       readonly=1)
    question_three_choice = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                             string="Choice",
                                             default='no')

    """ Question Four
        Yes: Open the treatment outside of ICSI from and add a record in the previous treatment history 
        No: move to next question
        
        -- Removed in the meeting 24-10-2023
    """
    question_four_label = fields.Char(string="Question 4:",
                                      default="What is the purpose of today’s visit?",
                                      store=False,
                                      readonly=1)

    ''' Additional questions '''
    is_couple_living_together = fields.Selection(selection=StaticMember.CHOICE_YES_NO_NA,
                                                 string="Is the couple living together?")

    is_couple_using_contraception = fields.Selection(selection=StaticMember.CHOICE_YES_NO_NA,
                                                     string="Is the couple using contraception?")

    """
        Ultrasound
        Abdominal
        TVS
    """
    repeat_ultrasound_type = fields.Selection(selection=StaticMember.ULTRASOUND_TYPE,
                                              string="Ultrasound")

    repeat_location_id = fields.Many2one(comodel_name='ec.medical.health.center',
                                         string='Location')

    repeat_status = fields.Selection(selection=StaticMember.REPEAT_STATUS,
                                     string='Status')

    repeat_consultation_interaction = fields.Selection(selection=StaticMember.REPEAT_CONSULTATION_TYPE,
                                                       string='Interaction')

    lmp_question_four = fields.Date(string='LMP')  # using above one here.
    repeat_cycle_day = fields.Integer(string='Cycle Day',
                                      readonly=True,
                                      store=True)

    repeat_date = fields.Datetime(string='Consultation Date',
                                  readonly=True,
                                  default=fields.Datetime.now)

    repeat_seen_by = fields.Many2one(comodel_name='res.users',
                                     string='Seen by',
                                     readonly=True,
                                     default=lambda self: self.env.user)

    repeat_other_doctors_present = fields.Many2many(comodel_name='res.consultant',
                                                    string='Other Doctors Present')
    ''' Seen with list required '''
    repeat_consultation_with = fields.Selection(selection=StaticMember.SEEN_WITH,
                                                string='Consultation with')

    repeat_seen_with_other = fields.Text(string='Other Present')

    # Define TVS field as per your TVS form structure
    # TVS = fields.Many2one('tvs.form', string='TVS Form')

    repeat_diagnosis = fields.Many2many(comodel_name='ec.medical.diagnosis',
                                        relation="ec_medical_repeat_diagnosis_rel",
                                        column1="repeat_id",
                                        column2="diagnosis_id",
                                        string="Diagnosis")

    repeat_treatment_plan = fields.Html(string='Plan')

    repeat_note = fields.Html(string="Reason for visit / Couple concerns / History of presenting complaints")

    repeat_investigations_ids = fields.Many2many(comodel_name='ec.medical.investigation',
                                                 relation="repeat_consultation_medical_investigation_rel",
                                                 column1="repeat_consultation_id",
                                                 column2="investigation_id",
                                                 string='Investigations')

    repeat_treatment_advised_ids = fields.Many2many(comodel_name='ec.medical.treatment.list',
                                                    relation="repeat_consultation_medical_treatment_list_rel",
                                                    column1="repeat_consultation_id",
                                                    column2="treatment_list_id",
                                                    string='Treatment Advised')

    repeat_examination_required = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                   string="Examination Required")

    repeat_gpe = fields.Text(string='GPE')
    repeat_thyroid = fields.Text(string="Thyroid")
    repeat_abdominal = fields.Text(string="Abdominal")
    repeat_breast = fields.Text(string="Breast")

    repeat_pelvic_examination_state = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                       string="Pelvic examination done?")

    repeat_examination_type = fields.Selection(selection=StaticMember.PELVIC_EXAM_CHOICES,
                                               string="Pelvic examination type")

    inspection_only = fields.Boolean(default=False,
                                     string="Inspection Only")

    p_v_only = fields.Boolean(default=False,
                              string="P/V")

    p_s_only = fields.Boolean(default=False,
                              string="P/S")

    repeat_findings_on_inspection = fields.Text(string="Findings on inspection")

    repeat_vaginal_exam = fields.Text(string='Vaginal Exam')
    repeat_valva_vaginal_exam = fields.Text(string='Valva and Vagina')
    repeat_cervix = fields.Text(string="Cervix")
    repeat_uterus_and_adnexae = fields.Text(string="Uterus and adnexae (bimanual)")

    # FIX: Remove this one only .
    repeat_swab_taken = fields.Boolean(string="Swab taken",
                                       default=False)

    repeat_hvs = fields.Boolean(string="HVS",
                                default=False)
    is_size = fields.Boolean('Size')
    is_position = fields.Boolean('Position')
    is_fiobrid = fields.Boolean('Fibroid')
    is_normal = fields.Boolean('Normal')

    female_repeat_uterus_length = fields.Selection(selection=StaticMember.GOITEAR_LENGTH, string='Uterus')
    female_repeat_uterus_width = fields.Selection(selection=StaticMember.GOITEAR_LENGTH, string='Uterus')

    repeat_endocervical = fields.Boolean(string="Endocervical",
                                         default=False)

    repeat_no_swab_taken = fields.Boolean(string="No swab taken",
                                          default=False)

    repeat_method_of_hvs = fields.Selection(string="Method of HVS",
                                            selection=StaticMember.METHOD_OF_HVS)

    repeat_pap_smear_done = fields.Boolean(string="Pap smear done",
                                           default=False)

    repeat_pipelle_sampling_done = fields.Boolean(string="Pipelle sampling done",
                                                  default=False)

    repeat_other_findings = fields.Text(string="Other findings")

    scan_required = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                     string="Scan required?")

    repeat_new_treatment_pathway = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                                    string="Start new treatment pathway")

    repeat_treatment_pathway = fields.Many2one(comodel_name='ec.medical.treatment.list',
                                               string='Treatment Pathway')

    counseling_and_discussion = fields.Html(string="Counseling and discussion done")

    '''Repeat Computed'''

    repeat_cyst_computed = fields.Html(string='Cyst', compute='repeat_values_compute')
    repeat_uterus_fibroid_computed = fields.Html(string='Uterus Fibroid', compute='repeat_values_compute')

    ''' Override methods '''

    def name_get(self):
        result = []
        for record in self:
            name = f"Repeat Consultation- {record.create_date.date()} - {record.repeat_patient_id.name}"
            result.append((record.id, name))
        return result

    ''' Data methods '''

    def repeat_values_compute(self):
        if self:
            for repeat in self:
                if repeat.repeat_timeline_id.tvs_cyst_size_ids:
                    table_rows = []
                    for record in repeat.repeat_timeline_id.tvs_cyst_size_ids:
                        type_value = record.type or '-'
                        size_x_value = str(record.generic_size_x) if record.generic_size_x is not None else '-'
                        size_y_value = str(record.generic_size_y) if record.generic_size_y is not None else '-'
                        table_row = f"<tr><td>{type_value}</td><td>{size_x_value},</td><td>(cm)</td></tr>"
                        table_rows.append(table_row)
                    dynamic_table = f"<table>{''.join(table_rows)}</table>"
                    repeat.repeat_cyst_computed = dynamic_table
                else:
                    repeat.repeat_cyst_computed = ''
                if repeat.repeat_timeline_id.tvs_generic_sizes_ids:
                    table_rows = []
                    for record in repeat.repeat_timeline_id.tvs_generic_sizes_ids:
                        size_x_value = str(record.generic_size_x) if record.generic_size_x is not None else '-'
                        size_y_value = str(record.generic_size_y) if record.generic_size_y is not None else '-'
                        table_row = f"<tr><td>{size_x_value},</td><td>{size_y_value}</td></tr>"
                        table_rows.append(table_row)
                    dynamic_table = f"<table>{''.join(table_rows)}</table>"
                    repeat.repeat_uterus_fibroid_computed = dynamic_table
                else:
                    repeat.repeat_uterus_fibroid_computed = ''


    def move_next(self):
        value = int(self.state)
        if value >= 4:
            return

        value += 1
        self.state = str(value)

    def move_back(self):
        value = int(self.state)
        if value <= 1:
            return

        value -= 1
        self.state = str(value)

    ''' Views/Action'''

    def action_open_form_view(self, patient_id, timeline_id):
        context = {
            'default_repeat_patient_id': patient_id.id,
            'default_repeat_timeline_id': timeline_id.id
        }

        return {
            "name": _("Repeat Consultation"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.repeat.consultation',
            'view_id': self.env.ref('ecare_medical_history.repeat_consultation_form_view').id,
            'view_mode': 'form',
            "target": 'current',
            'flags': {'initial_mode': 'edit'},
            'context': context,
        }

    def action_set_working_consultation(self):
        """
        It will make the consultation-editable on the patient.timeline
        """
        if self.repeat_timeline_id.show_repeat_section_state is True:
            raise UserError("Consultation is already in progress, close the running consultation first.")
        self.repeat_timeline_id.show_repeat_section_state = True
        if self.repeat_timeline_id.ec_repeat_consultation_id.id == self.id:
            return

        self.repeat_timeline_id.ec_repeat_consultation_id = self.id
        self.repeat_timeline_id.first_consultation_state = 'open'

    """ Other actions opening place over here"""

    def action_repeat_consultation_open_obstetrics_history(self):
        return self.env['ec.obstetrics.history'].action_open_form_view(self.repeat_patient_id,
                                                                       None)

    def action_repeat_consultation_open_previous_treatment(self):
        return self.env['ec.medical.previous.treatment'].action_open_form_view(self.repeat_patient_id)

    def action_open_tvs_form(self):
        return self.env['ec.medical.tvs'].action_open_form_view(self, target='new')

    def action_state_to_decision_pending(self):
        if self:
            self.first_consultation_state = 'decision_pending'

    def check_field_values_as_red(self):
        check_red_values = (self.medical_consents_risk_assessment_id.check_field_values_as_red() or
                            self.male_ot_ti_checklist_id.check_field_values_as_red() or
                            self.female_ot_ti_checklist_id.check_field_values_as_red())
        if check_red_values:
            return True
        else:
            return False

    def check_field_values_as_blue(self):
        check_blue_values = (self.female_ot_ti_checklist_id.check_field_values_as_blue())
        if check_blue_values:
            return True
        else:
            return False


# Fibroid
class RepeatFiobrid(models.Model):
    _name = 'ec.repeat.fiobrid'
    _description = "Patient Repeat Fiobrid"

    repeat_id = fields.Many2one('ec.repeat.consultation')

    length = fields.Integer('Length')
    width = fields.Integer('Width')

