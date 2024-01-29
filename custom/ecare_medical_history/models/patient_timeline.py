from datetime import datetime

from odoo import models, fields, api, _
from odoo.addons.ecare_core.utilities.helper import TimeValidation
import re
from odoo.addons.ecare_core.utilities.time_conversion import CustomDateTime

from odoo.exceptions import AccessError, UserError, ValidationError
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_medical_history.utils.validation import Validation


class PatientTimeline(models.Model):
    _name = "ec.patient.timeline"
    _description = "Patient Timeline"
    _rec_name = "timeline_patient_id"

    _sql_constraints = [
        ('timeline_patient_id_unique', 'unique (timeline_patient_id)',
         "Multiple patient timelines can't be created, rather open the existing one!"),
    ]

    _inherits = {
        'ec.first.consultation': 'ec_first_consultation_id',
        'ec.repeat.consultation': 'ec_repeat_consultation_id'
    }

    ''' FK's to build inherits '''
    ec_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete='restrict')
    ec_repeat_consultation_id = fields.Many2one(comodel_name="ec.repeat.consultation", ondelete='cascade')

    ''' Foreign keys '''
    timeline_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                          string="Patient",
                                          index=True)

    ''' FK's related-attributes '''

    ec_first_consultation_create_date = fields.Datetime("Create Date",
                                                        related='ec_first_consultation_id.create_date')

    ec_first_consultation_create_uid = fields.Many2one(string="Create User",
                                                       comodel_name='res.users',
                                                       related='ec_first_consultation_id.create_uid')

    ''' Patient attributes '''

    # Related Fields which are used for kanban view
    # Related Fields Used for data representation purposes
    timeline_patient_mr_num = fields.Char('MR No.', related="timeline_patient_id.mr_num")
    timeline_patient_name = fields.Char('Patient Name', related="timeline_patient_id.name")
    timeline_patient_wife_name = fields.Char('Wife Name', related="timeline_patient_id.wife_name")
    timeline_patient_husband_name = fields.Char('Husband Name', related="timeline_patient_id.husband_name")

    timeline_patient_mobile_wife = fields.Char('Mobile Wife', related="timeline_patient_id.mobile_wife")
    timeline_patient_mobile_husband = fields.Char('Husband Wife', related="timeline_patient_id.mobile_husband",)

    timeline_patient_wife_image = fields.Binary('Patient Wife Image', related="timeline_patient_id.image_1920")
    timeline_patient_husband_image = fields.Binary('Patient Husband Image', related="timeline_patient_id.husband_image")

    """ OBS History Relational Field"""

    first_obs_history_ids = fields.One2many(comodel_name='ec.obstetrics.history',
                                            inverse_name='timeline_id',
                                            string='Obstetrics History',
                                            )

    repeat_obs_history_ids = fields.One2many(comodel_name='ec.obstetrics.history',
                                             inverse_name='timeline_id',
                                             string='Obstetrics History',
                                             )

    """ Previous Treatment Relational Field See details in data/notes.md """

    timeline_previous_treatment_ids = fields.One2many(comodel_name='ec.medical.previous.treatment',
                                                      inverse_name='timeline_id',
                                                      string='Previous Treatment',
                                                      )

    first_previous_treatment_ids = fields.One2many(comodel_name='ec.medical.previous.treatment',
                                                   inverse_name='timeline_id',
                                                   string='Previous Treatment',
                                                   )

    repeat_previous_treatment_ids = fields.One2many(comodel_name='ec.medical.previous.treatment',
                                                    inverse_name='timeline_id',
                                                    string='Previous Treatment',
                                                    )

    ''' Related Fields'''
    patient_female_dob = fields.Date(string='CNIC DOB', store=True,
                                     related="timeline_patient_id.wife_dob")
    patient_male_dob = fields.Date(string='CNIC DOB', store=True,
                                   related="timeline_patient_id.husband_dob")

    # first_consultation_state = fields.Selection([('open', 'In Progress'),
    #                                              ('closed', 'Done'),
    #                                              ('decision_pending', "Decision Pending"),
    #                                              ],
    #                                             string='State',
    #                                             related="ec_first_consultation_id.first_consultation_state")
    ''' One2Many'''

    repeat_consultation_ids = fields.One2many(comodel_name="ec.repeat.consultation",
                                              inverse_name="repeat_timeline_id")

    ''' To control when to show '''

    show_repeat_section_state = fields.Boolean(default=False, string='Div State')
    show_repeat_consultation_history_section = fields.Boolean(default=False)

    ''' Many2many '''

    # Factors
    female_factor_ids = fields.Many2many(comodel_name='ec.medical.factors',
                                         relation="timeline_female_factor_rel",
                                         column1="timeline_id",
                                         column2="female_factor_id",
                                         domain=[('type', 'in', ['female'])])
    male_factor_ids = fields.Many2many(comodel_name='ec.medical.factors',
                                       relation="timeline_male_factor_rel",
                                       column1="timeline_id", column2="male_factor_id",
                                       domain=[('type', 'in', ['male'])])

    ''' Computed '''

    gravida_w = fields.Char(string='Gravida', compute='_compute_female_values')
    parity_x = fields.Char(string='Parity', compute='_compute_female_values')
    miscarriages_y = fields.Char(string='Miscarriages', compute='_compute_female_values')
    alive_z = fields.Char(string='Alive', compute='_compute_female_values')

    male_family_history = fields.Char(string='Male Family History', compute='_compute_family_history')
    female_family_history = fields.Char(string='Female Family History', compute='_compute_family_history')

    infertility_type = fields.Char(readonly=True, compute="_compute_infertility_type")

    ''' Data members '''
    timeline_conclusion = fields.Html(string="Conclusion")

    patient_attachment_ids = fields.One2many(string='Attachments',
                                         comodel_name='ec.medical.patient.attachment',
                                         inverse_name='patient_attachment_timeline_id')

    ''' Static methods '''
    @staticmethod
    def _compute_patient_family_history(family_history, fields_to_process):
        if not family_history:
            return None

        family_history_text = []

        for field_name, (field_label, custom_field_name) in fields_to_process.items():
            field_records = getattr(family_history, field_name)
            custom_field = getattr(family_history, custom_field_name)
            if field_name in ('male_family_history_other', 'female_family_history_other'):
                family_members_list = field_records
                if family_members_list:
                    field_text = f'<strong style="font-weight: 700;">{field_label}</strong><br>{family_members_list}'
                    family_history_text.append(field_text)
            elif field_records or (custom_field and custom_field.strip()):
                custom_text = f' ({custom_field.strip()})' if custom_field else ''
                family_members_list = [rec.name for rec in field_records]
                if family_members_list:
                    field_text = f'<strong style="font-weight: 700;">{field_label}</strong><br>{", ".join(family_members_list)}{custom_text}'
                    family_history_text.append(field_text)

        if family_history_text:
            family_history_text = '<br>'.join(family_history_text)
            return family_history_text

        return None

    ''' Computed methods '''

    @api.onchange('repeat_date', 'lmp_question_four')
    def _compute_cycle_day(self):
        """
        This is the onchange on the repeat consultation form.
        Formula: (Consultation Date - LMP) + 1
        :return: cycle day
        """
        if self.lmp_question_four:
            if CustomDateTime.greater_than_today(self.lmp_question_four):
                self.lmp_question_four = None
                raise ValidationError(_(
                    "Date can't be greater than current date!"))

            cycle_day = (self.repeat_date.date() - self.lmp_question_four).days
            cycle_day += 1

            self.repeat_cycle_day = cycle_day
            self.tvs_cycle_day = cycle_day
        else:
            self.repeat_cycle_day = 0
            self.tvs_cycle_day = 0

    def _compute_female_values(self):
        """
        Gravida: Total number of records in the obs.history
        Miscarriages: Before 24 and mode_of_delivery == "MISCARRIAGE"
        Parity: Total number of records in obs.history but duration of pregnancy >= 24

        :return: Set value to the gravida, parity and miscarriage attributes
        """

        gravida, parity, miscarriages, alive = 0, 0, 0, 0

        obs_histories = self.env['ec.obstetrics.history'].search([
            ('patient_id', '=', self.timeline_patient_id.id)
        ])

        if not obs_histories:
            self.gravida_w = 0
            self.parity_x = 0
            self.miscarriages_y = miscarriages
            self.alive_z = alive
            return

        pregnancies = len(obs_histories)
        count_after_24_weeks = 0 # Or parity
        for obs_history in obs_histories:
            dop = obs_history.duration_of_pregnancy.replace("<", "").replace(">", "") \
                if obs_history.duration_of_pregnancy else None

            if dop:
                dop = int(dop)

                if dop >= 24:
                    count_after_24_weeks += 1
                if dop < 24 and obs_history.mode_of_delivery == 'MISCARRIAGE':
                    miscarriages += 1

            if obs_history.alive == 'Alive':
                alive += 1


        self.gravida_w = pregnancies
        self.parity_x = count_after_24_weeks
        self.miscarriages_y = miscarriages
        self.alive_z = alive

    def _compute_family_history(self):
        # Male Fields Processing

        male_fields_to_process = {
            'male_diabetes_ids': ('Diabetes', 'male_other_diabetes'),
            'male_malignancies_ids': ('Malignancies', 'male_other_malignancies'),
            'male_hypertension_ids': ('Hypertension', 'male_other_hypertension'),
            'male_mental_illness_ids': ('Mental Illness', 'male_other_mental_illness'),
            'male_twins_ids': ('Twins', 'male_other_twins'),
            'male_tuberculosis_ids': ('Tuberculosis', 'male_other_tuberculosis'),
            'male_abnormalities_ids': ('Congenital Abnormalities', 'male_other_abnormalities'),
            'male_family_history_other': ('Other History', 'male_family_history_other')
        }

        self.male_family_history = PatientTimeline._compute_patient_family_history(
            family_history=self.ec_first_consultation_id.ec_male_family_history_id,
            fields_to_process=male_fields_to_process
        )

        # Female Fields Processing

        fields_to_process = {
            'female_diabetes_ids': ('Diabetes', 'female_other_diabetes'),
            'female_malignancies_ids': ('Malignancies', 'female_other_malignancies'),
            'female_hypertension_ids': ('Hypertension', 'female_other_hypertension'),
            'female_mental_illness_ids': ('Mental Illness', 'female_other_mental_illness'),
            'female_tuberculosis_ids': ('Tuberculosis', 'female_other_tuberculosis'),
            'female_abnormalities_ids': ('Congenital Abnormalities', 'female_other_abnormalities'),
            'female_twins_ids': ('Twins', 'female_other_twins'),
            'female_pregnancy_induced_hypertension_ids': (
                'Pregnancy Induced Hypertension', 'female_other_pregnancy_induced_hypertension'),
            'female_miscarriage_ids': ('Miscarriages', 'female_other_miscarriage'),
            'female_preterm_birth_ids': ('Preterm Births', 'female_other_preterm_birth'),
            'female_still_birth_ids': ('Still Births', 'female_other_still_birth'),
            'female_pre_mature_ovarian_failure_ids': (
                'Pre-mature Ovarian Failure', 'female_other_pre_mature_ovarian_failure'),
            'female_family_history_other': ('Other History', 'female_family_history_other')
        }

        self.female_family_history = PatientTimeline._compute_patient_family_history(
            family_history=self.ec_first_consultation_id.ec_female_family_history_id,
            fields_to_process=fields_to_process
        )

    def _compute_infertility_type(self):
        for record in self:
            if len(record.first_obs_history_ids) > 0:
                record.infertility_type = StaticMember.INFERTILITY[1][1]
            else:
                record.infertility_type = StaticMember.INFERTILITY[0][1]

    ''' Override methods '''

    @api.model
    def create(self, vals):
        res = super(PatientTimeline, self).create(vals)
        res.ec_repeat_consultation_id.update(
            res._get_repeat_consultation_mandatory_attribute()
        )
        res.populate_dependent_patient_field()

        return res

    ''' XXX - Override methods - XXX'''

    ''' Onchange methods '''
    @api.onchange("timeline_patient_id")
    def populate_dependent_patient_field(self):
        """
            We are only updating the first_consultation, and in the hind case, it'll trigger all other patients
        """
        for record in self:
            patient_id = record.timeline_patient_id
            record.first_consultation_patient_id = patient_id
            record.ec_first_consultation_id.populate_all_patients()
            # record.first_consultation_patient_id.populate_all_patients()

    @api.onchange('biological_female_dob')
    def _get_biological_age_female(self):
        for rec in self:
            rec.biological_female_age = TimeValidation.convert_date_to_days_years(rec.biological_female_dob)

    @api.onchange('biological_male_dob')
    def _get_biological_age_male(self):
        for rec in self:
            rec.biological_male_age = TimeValidation.convert_date_to_days_years(rec.biological_male_dob)

    """
    Action for opening views
    *. Please put all the actions over here which open any kind of views
    """

    def action_open_patient_time_view(self):
        patient_id = self.env.context.get('0')
        return {
            'name': 'Patient',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'res_model': 'ec.medical.patient',
            'res_id': patient_id,
            'target': 'new',
        }

    def action_timeline_open_obstetrics_history(self):
        return self.env['ec.obstetrics.history'].action_open_form_view(self.timeline_patient_id,
                                                                       self)

    def action_timeline_open_treatment_history(self):
        return self.env['ec.medical.previous.treatment'].action_open_form_view(self.timeline_patient_id,
                                                                               self)

    def action_create_repeat_consultation(self):
        self.show_repeat_section_state = True
        if self.show_repeat_consultation_history_section is False:
            self.show_repeat_consultation_history_section = True
            if self.ec_repeat_consultation_id:
                self.repeat_consultation_ids.repeat_date = datetime.now()
            return

        repeat_consultation_id = self.env['ec.repeat.consultation'].create(
            self._get_repeat_consultation_mandatory_attribute()
        )
        self.ec_repeat_consultation_id = repeat_consultation_id.id
        # return self.env['ec.repeat.consultation'].action_open_form_view(self.timeline_patient_id, self)

    ''' Action for opening views block ended '''

    def action_mandatory_patient_timeline(self, patient):
        timeline_rec = {
            'first_consultation_patient_id': patient.id,
            'timeline_patient_id': patient.id,
        }

        return timeline_rec

    def action_create_timeline_from_patient(self, patient):
        values = self.action_mandatory_patient_timeline(patient)
        if not patient.mr_num:
            raise UserError("Patient MR No. is not  generated yet, please generate MR No. for this patient first.")
        patient_timeline_id = self.env['ec.patient.timeline'].create(values)
        return patient_timeline_id

    def action_open_tvs_form(self):
        return self.env['ec.medical.tvs'].action_open_form_view(self.ec_repeat_consultation_id)

    def action_repeat_consultation_open_previous_treatment(self):
        return self.env['ec.medical.previous.treatment'].action_open_form_view(self)

    def action_close_first_consultation(self):
        return self.env['ec.first.consultation'].action_close_first_consultation(self.ec_first_consultation_id)

    def action_open_first_consultation(self):
        return self.env['ec.first.consultation'].action_open_first_consultation(self.ec_first_consultation_id)

    def action_repeat_consultation_open_obstetrics_history(self):
        return self.env['ec.obstetrics.history'].action_open_form_view(self.timeline_patient_id,
                                                                       None)
    def action_open_seminology(self):
        return self.env['ec.semen.analysis'].action_open_form_view(self.timeline_patient_id)

    def action_open_tvs_scan(self):
        return self.ec_repeat_consultation_id.repeat_tvs_id.action_open_tvs_scan()

    ''' Data methods '''

    def _get_repeat_consultation_mandatory_attribute(self):
        patient_id = self.timeline_patient_id.id
        return {
            'repeat_timeline_id': self.id,
            'repeat_patient_id': patient_id,
            'tvs_patient_id': patient_id,
            'tvs_repeat_consultation_id': self.id
        }

    def move_next(self):
        value = int(self.repeat_state)
        if value >= 4:
            return

        value += 1
        self.repeat_state = str(value)

    def move_back(self):
        value = int(self.repeat_state)
        if value <= 1:
            return

        value -= 1
        self.repeat_state = str(value)

    def action_save_repeat_consultation_section(self):
        self.show_repeat_section_state = False
        self.ec_repeat_consultation_id.first_consultation_state = 'closed'

    @api.onchange('female_lmp')
    def _check_female_lmp_date(self):
        if self.female_lmp:
            return Validation._date_validation(self.female_lmp)

    @api.onchange('biological_female_dob')
    def _check_biological_female_dob_date(self):
        if self.biological_female_dob:
            return Validation._date_validation(self.biological_female_dob)

    @api.onchange('biological_male_dob')
    def _check_biological_male_dob_date(self):
        if self.biological_male_dob:
            return Validation._date_validation(self.biological_male_dob)

    @api.onchange('gynaecological_examination_lmp')
    def _check_gynaecological_examination_lmp_date(self):
        if self.gynaecological_examination_lmp:
            return Validation._date_validation(self.gynaecological_examination_lmp)

    @api.onchange('gynaecological_examination_date')
    def _check_gynaecological_examination_date_date(self):
        if self.gynaecological_examination_date:
            return Validation._date_validation(self.gynaecological_examination_date)

    @api.onchange('repeat_pregnancy_lmp')
    def _check_repeat_pregnancy_lmp_date(self):
        if self.repeat_pregnancy_lmp:
            return Validation._date_validation(self.repeat_pregnancy_lmp)

    @api.onchange('repeat_pregnancy_procedure_performed')
    def _computed_procedure_performed_text(self):
        if self.repeat_pregnancy_procedure_performed:
            self.repeat_pregnancy_procedure_performed_text = ''
            self.repeat_pregnancy_procedure_performed_text = self.repeat_pregnancy_procedure_performed.value
        else:
            self.repeat_pregnancy_procedure_performed_text = ''

    @api.onchange('female_adrenal_date')
    def _check_female_adrenal_date(self):
        if self.female_adrenal_date:
            return Validation._year_validation(self.female_adrenal_date)

    @api.onchange('female_anti_phospholipid_syndrome_date')
    def _check_female_anti_phospholipid_syndrome_date(self):
        if self.female_anti_phospholipid_syndrome_date:
            return Validation._year_validation(self.female_anti_phospholipid_syndrome_date)

    @api.onchange('female_autoimmune_disease_date')
    def _check_female_autoimmune_disease_date(self):
        if self.female_autoimmune_disease_date:
            return Validation._year_validation(self.female_autoimmune_disease_date)

    @api.onchange('female_blood_transfusion_date')
    def _check_female_blood_transfusion_date(self):
        if self.female_blood_transfusion_date:
            return Validation._year_validation(self.female_blood_transfusion_date)

    @api.onchange('female_cardiac_date')
    def _check_female_cardiac_date(self):
        if self.female_cardiac_date:
            return Validation._year_validation(self.female_cardiac_date)

    @api.onchange('female_gall_bladder_date')
    def _check_female_gall_bladder_date(self):
        if self.female_gall_bladder_date:
            return Validation._year_validation(self.female_gall_bladder_date)

    @api.onchange('female_gastric_date')
    def _check_female_gastric_date(self):
        if self.female_gastric_date:
            return Validation._year_validation(self.female_gastric_date)

    @api.onchange('female_gynaecology_date')
    def _check_female_gynaecology_date(self):
        if self.female_gynaecology_date:
            return Validation._year_validation(self.female_gynaecology_date)

    @api.onchange('female_haematology_date')
    def _check_female_haematology_date(self):
        if self.female_haematology_date:
            return Validation._year_validation(self.female_haematology_date)

    @api.onchange('female_intestinal_date')
    def _check_female_intestinal_date(self):
        if self.female_intestinal_date:
            return Validation._year_validation(self.female_intestinal_date)

    @api.onchange('female_liver_date')
    def _check_female_liver_date(self):
        if self.female_liver_date:
            return Validation._year_validation(self.female_liver_date)

    @api.onchange('female_low_urinary_tract_date')
    def _check_female_low_urinary_tract_date(self):
        if self.female_low_urinary_tract_date:
            return Validation._year_validation(self.female_low_urinary_tract_date)

    @api.onchange('female_malignancy_date')
    def _check_female_malignancy_date(self):
        if self.female_malignancy_date:
            return Validation._year_validation(self.female_malignancy_date)

    @api.onchange('female_neurological_date')
    def _check_female_neurological_date(self):
        if self.female_neurological_date:
            return Validation._year_validation(self.female_neurological_date)

    @api.onchange('female_renal_date')
    def _check_female_renal_date(self):
        if self.female_renal_date:
            return Validation._year_validation(self.female_renal_date)

    @api.onchange('female_respiratory_date')
    def _check_female_respiratory_date(self):
        if self.female_respiratory_date:
            return Validation._year_validation(self.female_respiratory_date)

    @api.onchange('female_skeletal_date')
    def _check_female_skeletal_date(self):
        if self.female_skeletal_date:
            return Validation._year_validation(self.female_skeletal_date)

    @api.onchange('female_thyroid_date')
    def _check_female_thyroid_date(self):
        if self.female_thyroid_date:
            return Validation._year_validation(self.female_thyroid_date)

    @api.onchange('female_heart_disease_date')
    def _check_female_heart_disease_date(self):
        if self.female_heart_disease_date:
            return Validation._year_validation(self.female_heart_disease_date)

    @api.onchange('female_urinary_infection_date')
    def _check_female_urinary_infection_date(self):
        if self.female_urinary_infection_date:
            return Validation._year_validation(self.female_urinary_infection_date)

    @api.onchange('female_hyper_tension_date')
    def _check_female_hyper_tension_date(self):
        if self.female_hyper_tension_date:
            return Validation._year_validation(self.female_hyper_tension_date)

    @api.onchange('female_janduice_date')
    def _check_female_janduice_date(self):
        if self.female_janduice_date:
            return Validation._year_validation(self.female_janduice_date)

    @api.onchange('female_diabetes_date')
    def _check_female_diabetes_date(self):
        if self.female_diabetes_date:
            return Validation._year_validation(self.female_diabetes_date)

    @api.onchange('female_dvt_date')
    def _check_female_dvt_date(self):
        if self.female_dvt_date:
            return Validation._year_validation(self.female_dvt_date)

    @api.onchange('female_smoking_date')
    def _check_female_smoking_date(self):
        if self.female_smoking_date:
            return Validation._year_validation(self.female_smoking_date)

    @api.onchange('female_alcohol_date')
    def _check_female_alcohol_date(self):
        if self.female_alcohol_date:
            return Validation._year_validation(self.female_alcohol_date)

    @api.onchange('female_medical_history_others_date')
    def _check_female_medical_history_others_date(self):
        if self.female_medical_history_others_date:
            return Validation._year_validation(self.female_medical_history_others_date)

    @api.onchange('male_adrenal_date')
    def _check_male_adrenal_date(self):
        if self.male_adrenal_date:
            return Validation._year_validation(self.male_adrenal_date)

    @api.onchange('male_anti_phospholipid_syndrome_date')
    def _check_male_anti_phospholipid_syndrome_date(self):
        if self.male_anti_phospholipid_syndrome_date:
            return Validation._year_validation(self.male_anti_phospholipid_syndrome_date)

    @api.onchange('male_autoimmune_disease_date')
    def _check_male_autoimmune_disease_date(self):
        if self.male_autoimmune_disease_date:
            return Validation._year_validation(self.male_autoimmune_disease_date)

    @api.onchange('male_blood_transfusion_date')
    def _check_male_blood_transfusion_date(self):
        if self.male_blood_transfusion_date:
            return Validation._year_validation(self.male_blood_transfusion_date)

    @api.onchange('male_cardiac_date')
    def _check_male_cardiac_date(self):
        if self.male_cardiac_date:
            return Validation._year_validation(self.male_cardiac_date)

    @api.onchange('male_gall_bladder_date')
    def _check_male_gall_bladder_date(self):
        if self.male_gall_bladder_date:
            return Validation._year_validation(self.male_gall_bladder_date)

    @api.onchange('male_gastric_date')
    def _check_male_gastric_date(self):
        if self.male_gastric_date:
            return Validation._year_validation(self.male_gastric_date)

    @api.onchange('male_gynaecology_date')
    def _check_male_gynaecology_date(self):
        if self.male_gynaecology_date:
            return Validation._year_validation(self.male_gynaecology_date)

    @api.onchange('male_haematology_date')
    def _check_male_haematology_date(self):
        if self.male_haematology_date:
            return Validation._year_validation(self.male_haematology_date)

    @api.onchange('male_intestinal_date')
    def _check_male_intestinal_date(self):
        if self.male_intestinal_date:
            return Validation._year_validation(self.male_intestinal_date)

    @api.onchange('male_liver_date')
    def _check_male_liver_date(self):
        if self.male_liver_date:
            return Validation._year_validation(self.male_liver_date)

    @api.onchange('male_low_urinary_tract_date')
    def _check_male_low_urinary_tract_date(self):
        if self.male_low_urinary_tract_date:
            return Validation._year_validation(self.male_low_urinary_tract_date)

    @api.onchange('male_malignancy_date')
    def _check_male_malignancy_date(self):
        if self.male_malignancy_date:
            return Validation._year_validation(self.male_malignancy_date)

    @api.onchange('male_neurological_date')
    def _check_male_neurological_date(self):
        if self.male_neurological_date:
            return Validation._year_validation(self.male_neurological_date)

    @api.onchange('male_renal_date')
    def _check_male_renal_date(self):
        if self.male_renal_date:
            return Validation._year_validation(self.male_renal_date)

    @api.onchange('male_respiratory_date')
    def _check_male_respiratory_date(self):
        if self.male_respiratory_date:
            return Validation._year_validation(self.male_respiratory_date)

    @api.onchange('male_skeletal_date')
    def _check_male_skeletal_date(self):
        if self.male_skeletal_date:
            return Validation._year_validation(self.male_skeletal_date)

    @api.onchange('male_thyroid_date')
    def _check_male_thyroid_date(self):
        if self.male_thyroid_date:
            return Validation._year_validation(self.male_thyroid_date)

    @api.onchange('male_heart_disease_date')
    def _check_male_heart_disease_date(self):
        if self.male_heart_disease_date:
            return Validation._year_validation(self.male_heart_disease_date)

    @api.onchange('male_urinary_infection_date')
    def _check_male_urinary_infection_date(self):
        if self.male_urinary_infection_date:
            return Validation._year_validation(self.male_urinary_infection_date)

    @api.onchange('male_hyper_tension_date')
    def _check_male_hyper_tension_date(self):
        if self.male_hyper_tension_date:
            return Validation._year_validation(self.male_hyper_tension_date)

    @api.onchange('male_janduice_date')
    def _check_male_janduice_date(self):
        if self.male_janduice_date:
            return Validation._year_validation(self.male_janduice_date)

    @api.onchange('male_diabetes_date')
    def _check_male_diabetes_date(self):
        if self.male_diabetes_date:
            return Validation._year_validation(self.male_diabetes_date)

    @api.onchange('male_dvt_date')
    def _check_male_dvt_date(self):
        if self.male_dvt_date:
            return Validation._year_validation(self.male_dvt_date)

    @api.onchange('male_smoking_date')
    def _check_male_smoking_date(self):
        if self.male_smoking_date:
            return Validation._year_validation(self.male_smoking_date)

    @api.onchange('male_alcohol_date')
    def _check_male_alcohol_date(self):
        if self.male_alcohol_date:
            return Validation._year_validation(self.male_alcohol_date)

    @api.onchange('male_medical_history_others_date')
    def _check_male_medical_history_others_date(self):
        if self.male_medical_history_others_date:
            return Validation._year_validation(self.male_medical_history_others_date)

    @api.onchange('female_weight', 'female_height')
    def _calculate_physical_exam_bmi(self):
        if self.female_weight and self.female_height:
            height_in_meters = self.female_height / 100
            self.female_bmi = self.female_weight / (height_in_meters ** 2)
        else:
            self.female_bmi = None

    @api.onchange('repeat_pregnancy_lmp')
    def _compute_gestational_age(self):
        for rec in self:
            date_analysis = rec.create_date
            lmp = rec.repeat_pregnancy_lmp
            if date_analysis and lmp:
                diff = date_analysis.date() - lmp
                weeks = int(diff.days) // 7
                weeks = abs(weeks)
                if 1 < weeks <= 40:
                    if 1 <= weeks <= 9:
                        rec.repeat_pregnancy_gestational_age = str(int(weeks))
                    else:
                        rec.repeat_pregnancy_gestational_age = str(int(weeks))
                else:
                    rec.repeat_pregnancy_gestational_age = '>40'
            else:
                rec.repeat_pregnancy_gestational_age = None

    @api.onchange('repeat_pregnancy_temp')
    def _check_float_input_temp(self):
        if self.repeat_pregnancy_temp and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_temp):
            raise UserError(f"Please enter a numeric value in pregnancy temperature.")
            # raise UserError(f"Please enter a numeric value in pregnancy temperature with up to 2 decimal points.")

    @api.onchange('repeat_pregnancy_hr')
    def _check_float_input_hr(self):
        if self.repeat_pregnancy_hr and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_hr):
            raise UserError(f"Please enter a numeric value in pregnancy HR.")

    @api.onchange('repeat_pregnancy_bp_upper')
    def _check_float_input_bp_upper(self):
        if self.repeat_pregnancy_bp_upper and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.repeat_pregnancy_bp_upper):
            raise UserError(f"Please enter a numeric value in pregnancy BP (Upper).")

    @api.onchange('repeat_pregnancy_bp_lower')
    def _check_float_input_bp_lower(self):
        if self.repeat_pregnancy_bp_lower and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.repeat_pregnancy_bp_lower):
            raise UserError(f"Please enter a numeric value in pregnancy BP (Lower).")

    @api.onchange('repeat_pregnancy_rr')
    def _check_float_input_rr(self):
        if self.repeat_pregnancy_rr and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_rr):
            raise UserError(f"Please enter a numeric value in pregnancy RR.")

    @api.onchange('repeat_pregnancy_embryos_replaced')
    def _check_input_repeat_pregnancy_embryos_replaced(self):
        if self.repeat_pregnancy_embryos_replaced and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_embryos_replaced):
            raise UserError(f"Please enter a numeric value in pregnancy embryos replaced!")

    @api.onchange('female_weight')
    def _check_input_female_weight(self):
        if self.female_weight and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_weight):
            raise UserError(f"Please enter a numeric value in female weight!")

    @api.onchange('female_height')
    def _check_input_female_height(self):
        if self.female_height and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_height):
            raise UserError(f"Please enter a numeric value in female height!")

    @api.onchange('female_bmi')
    def _check_input_female_bmi(self):
        if self.female_bmi and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_bmi):
            raise UserError(f"Please enter a numeric value in female bmi!")

    @api.onchange('female_bp_upper')
    def _check_input_female_bp_upper(self):
        if self.female_bp_upper and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.female_bp_upper):
            raise UserError(f"Please enter a numeric value in female bp upper!")

    @api.onchange('female_bp_lower')
    def _check_input_female_bp_lower(self):
        if self.female_bp_lower and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.female_bp_lower):
            raise UserError(f"Please enter a numeric value in female bp lower!")

    @api.onchange('female_pulse')
    def _check_input_female_pulse(self):
        if self.female_pulse and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.female_pulse):
            raise UserError(f"Please enter a numeric value in female pulse!")

    @api.onchange('female_temperature')
    def _check_input_female_temperature(self):
        if self.female_temperature and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_temperature):
            raise UserError(f"Please enter a numeric value in female temperature!")

    @api.onchange('male_weight')
    def _check_input_male_weight(self):
        if self.male_weight and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_weight):
            raise UserError(f"Please enter a numeric value in male weight!")

    @api.onchange('male_height')
    def _check_input_male_height(self):
        if self.male_height and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_height):
            raise UserError(f"Please enter a numeric value in male height!")

    @api.onchange('male_bmi')
    def _check_input_male_bmi(self):
        if self.male_bmi and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_bmi):
            raise UserError(f"Please enter a numeric value in male bmi!")

    @api.onchange('male_bp_upper')
    def _check_input_male_bp_upper(self):
        if self.male_bp_upper and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.male_bp_upper):
            raise UserError(f"Please enter a numeric value in male bp upper!")

    @api.onchange('male_bp_lower')
    def _check_input_male_bp_lower(self):
        if self.male_bp_lower and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.male_bp_lower):
            raise UserError(f"Please enter a numeric value in male bp lower!")

    @api.onchange('male_pulse')
    def _check_input_male_pulse(self):
        if self.male_pulse and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.male_pulse):
            raise UserError(f"Please enter a numeric value in male pulse!")

    @api.onchange('male_temperature')
    def _check_input_male_temperature(self):
        if self.male_temperature and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_temperature):
            raise UserError(f"Please enter a numeric value in male temperature!")

    @api.onchange('biological_female_dob_check', 'biological_male_dob_check')
    def _check_same_as_above_functionality(self):
        if self.biological_female_dob_check:
            self.biological_female_dob = None
        if self.biological_male_dob_check:
            self.biological_male_dob = None
