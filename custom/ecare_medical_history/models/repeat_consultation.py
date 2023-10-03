from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from logging import getLogger
_logger = getLogger(__name__)


class RepeatConsultation(models.Model):
    _name = 'ec.repeat.consultation'
    _description = "Patient Repeat Consultation"

    ''' Foreign Keys '''

    patient_id = fields.Many2one(comodel_name="ec.medical.patient")
    timeline_id = fields.Many2one(comodel_name="ec.patient.timeline")

    ''' Data attributes '''

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
                                           default='no')

    lmp = fields.Date(string="LMP")
    lmp_embryo = fields.Date(string="LMP Embryo")

    """ Question Two
        Yes: Move to obstetrics 
        No: Move to next
    """
    question_two_label = fields.Char(string="Question 2:",
                                     default="Has the couple had any conception since the last visit?",
                                     store=False,
                                     readonly=1)
    question_two_choice = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                           string="Choice",
                                           default='no'
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
                                             default='no'
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
                              string='Status', default='walkin')

    consultation_type = fields.Selection(selection=StaticMember.REPEAT_CONSULTATION_TYPE, string='Consultation Type')

    # lmp_calendar = fields.Date(string='LMP')
    cycle_day = fields.Integer(string='Cycle Day', store=True)
    date = fields.Datetime(string='Date', default=fields.Datetime.now)
    seen_by = fields.Many2one('res.users', string='Seen by', default=lambda self: self.env.user)

    other_doctors_present = fields.Many2many('res.users', string='Other Doctors Present')
    seen_with = fields.Many2one('res.users', string='Seen with')

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

    investigations = fields.Many2many('ec.medical.investigation', string='Investigations')
    # treatment_advised = fields.Many2many('treatment.type', string='Treatment Advised')

    ''' Override methods '''

    def name_get(self):
        result = []
        for record in self:
            name = f"Repeat Consultation- {record.create_date.date()} - {record.patient_id.name}"
            result.append((record.id, name))
        return result

    ''' Data methods '''
    def move_next(self):
        value = int(self.state)
        if value > 4:
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
            'default_patient_id': patient_id.id,
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

    """ Other actions opening place over here"""
    def action_repeat_consultation_open_obstetrics_history(self):
        return self.env['ec.obstetrics.history'].action_open_form_view(self.patient_id,
                                                                       None)

    def action_repeat_consultation_open_previous_treatment(self):
        return self.env['ec.medical.previous.treatment'].action_previous_treatment_open_form_view(self.patient_id)

    def action_open_tvs_form(self):
        record = self.env['ec.medical.tvs'].search([(
            'repeat_consultation_id', '=', int(self.id)
        )], limit=1)
        if record:
            return {
                "name": _("TVS"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.medical.tvs',
                'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_form').id,
                'view_mode': 'form',
                "target": 'current',
                "res_id": record.id,
                'flags': {'initial_mode': 'edit'},
            }
        else:
            context = {
                'default_repeat_consultation_id': self.id,
            }
            return {
                "name": _("TVS"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.medical.tvs',
                'view_id': self.env.ref('ecare_medical_history.view_ec_medical_tvs_form').id,
                'view_mode': 'form',
                "target": 'current',
                'context': context,
            }
