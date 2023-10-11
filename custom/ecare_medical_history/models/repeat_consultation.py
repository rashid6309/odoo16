from odoo import api, models, fields, _
from odoo.exceptions import UserError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from logging import getLogger
_logger = getLogger(__name__)


class RepeatConsultation(models.Model):
    _name = 'ec.repeat.consultation'
    _description = "Patient Repeat Consultation"

    ''' Foreign Keys '''

    repeat_patient_id = fields.Many2one(comodel_name="ec.medical.patient")
    timeline_id = fields.Many2one(comodel_name="ec.patient.timeline", ondelete="restrict")

    ''' Data attributes '''
    ''' @FIX: state to repeat_consultation_state '''

    state = fields.Selection(selection=[('1', "Question 1"),
                                        ('2', "Question 2"),
                                        ('3', "Question 3"),
                                        ('4', "Question 4")],
                             default="1",
                             required=True)

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
                                           readonly=True,
                                           states={'1': [('readonly', False)]},
                                           default='no')

    lmp = fields.Date(string="LMP",
                      readonly=True,
                      states={'1': [('readonly', False)]},
                      )
    lmp_embryo = fields.Date(string="LMP Embryo",
                             readonly=True,
                             states = {'1': [('readonly', False)]}
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
                                           default='no',
                                           readonly=True,
                                           states={'2': [('readonly', False)]},
                                           )

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
                                             default='no',
                                             readonly=True,
                                             states={'3': [('readonly', False)]},
                                             )

    """ Question Four
        Yes: Open the treatment outside of ICSI from and add a record in the previous treatment history 
        No: move to next question

    """
    question_four_label = fields.Char(string="Question 4:",
                                      default="What is the purpose of today’s visit?",
                                      store=False,
                                      readonly=1)
    # question_four_choice = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
    #                                         default='no'
    #                                         )

    """
        Ultrasound
        Abdominal
        TVS
    """
    ultrasound_type = fields.Selection(selection=StaticMember.ULTRASOUND_TYPE,
                                       string="Ultrasound")

    location_id = fields.Many2one(comodel_name='ec.medical.health.center',
                                  string='Location')

    status = fields.Selection(selection=StaticMember.REPEAT_STATUS,
                              string='Status',
                              default='walkin')

    consultation_type = fields.Selection(selection=StaticMember.REPEAT_CONSULTATION_TYPE,
                                         string='Consultation Type')

    lmp_question_four = fields.Date(string='LMP') # using above one here.
    cycle_day = fields.Integer(string='Cycle Day', store=True)

    date = fields.Datetime(string='Date',
                           readonly=True,
                           default=fields.Datetime.now)

    seen_by = fields.Many2one(comodel_name='res.users',
                              string='Seen by',
                              readonly=True,
                              default=lambda self: self.env.user)

    other_doctors_present = fields.Many2many(comodel_name='res.consultant',
                                             string='Other Doctors Present')
    ''' Seen with list required '''
    seen_with = fields.Selection(selection=StaticMember.SEEN_WITH,
                                string='Seen with')

    notes = fields.Text(string='Notes')
    gpe_breast_abdominal_exam = fields.Text(string='GPE / Breast / Abdominal Exam')
    vaginal_exam = fields.Text(string='Vaginal Exam')

    # Define TVS field as per your TVS form structure
    # TVS = fields.Many2one('tvs.form', string='TVS Form')

    diagnosis = fields.Text(string='Diagnosis')
    advised = fields.Text(string='Advised')

    treatment_plan = fields.Selection(selection=StaticMember.REPEAT_TREATMENT_PLAN,
                                      string='Treatment Plan')

    procedure_plan = fields.Text(string='Procedure Plan')

    investigations_ids = fields.Many2many(comodel_name='ec.medical.investigation',
                                          relation="repeat_consultation_medical_investigation_rel",
                                          column1="repeat_consultation_id",
                                          column2="investigation_id",
                                          string='Investigations')

    treatment_advised_ids = fields.Many2many(comodel_name='ec.medical.treatment.list',
                                             relation="repeat_consultation_medical_treatment_list_rel",
                                             column1="repeat_consultation_id",
                                             column2="treatment_list_id",
                                             string='Treatment Advised')

    ''' Override methods '''

    def name_get(self):
        result = []
        for record in self:
            name = f"Repeat Consultation- {record.create_date.date()} - {record.repeat_patient_id.name}"
            result.append((record.id, name))
        return result

    ''' Data methods '''
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

    def action_open_form_view(self, patient_id, timeline_id):
        context = {
            'default_repeat_patient_id': patient_id.id,
            'default_timeline_id': timeline_id.id
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
        self.timeline_id.show_repeat_section_state = True
        if self.timeline_id.ec_repeat_consultation_id.id == self.id:
            raise UserError("Consultation is already selected.")

        self.timeline_id.ec_repeat_consultation_id = self.id

    """ Other actions opening place over here"""
    def action_repeat_consultation_open_obstetrics_history(self):
        return self.env['ec.obstetrics.history'].action_open_form_view(self.repeat_patient_id,
                                                                       None)

    def action_repeat_consultation_open_previous_treatment(self):
        return self.env['ec.medical.previous.treatment'].action_open_form_view(self.repeat_patient_id)

    def action_open_tvs_form(self):
        return self.env['ec.medical.tvs'].action_open_form_view(self, self.repeat_patient_id)