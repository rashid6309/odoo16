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

    create_date_first_consultation = fields.Datetime("Create Date",
                                                     default=lambda self: fields.Datetime.now())
    ec_create_date_first_consultation_computed = fields.Datetime("Create Date",
                                                                 readonly=True,
                                                                 store=True,
                                                                 conpute='ec_create_date_first_consultation')

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
    timeline_patient_mobile_husband = fields.Char('Husband Wife', related="timeline_patient_id.mobile_husband", )

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
    duplicated_lmp_question_four = fields.Date(string='LMP', related='ec_repeat_consultation_id.lmp_question_four')

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

    male_medical_history = fields.Char(string='Male Medical History', compute='_compute_medical_history')
    female_medical_history = fields.Char(string='Female Medical History', compute='_compute_medical_history')

    male_surgical_history = fields.Char(string='Male Surgical History', compute='_compute_surgical_history')
    female_surgical_history = fields.Char(string='Female Surgical History', compute='_compute_surgical_history')

    infertility_type = fields.Char(readonly=True, compute="_compute_infertility_type")

    ''' Data members '''

    ''' OI/TI Fields '''
    oi_ti_platform_enabled = fields.Boolean(string="OI/TI Platform", default=False)
    oi_ti_platform_cycle_ids = fields.One2many(comodel_name="ec.medical.oi.ti.platform.cycle",
                                               inverse_name="cycle_timeline_id",
                                               string="OI/TI Cycle/Attempt")

    patient_attachment_ids = fields.One2many(string='Attachments Details',
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

    @staticmethod
    def _compute_patient_medical_history(medical_history, fields_to_process):
        if not medical_history:
            return None

        medical_history_text = []

        for field_name, (field_label, custom_field_name) in fields_to_process.items():
            field_records = getattr(medical_history, field_name)
            custom_field = getattr(medical_history, custom_field_name)
            if field_records or (custom_field and custom_field.strip()):
                custom_text = f' {str(custom_field).strip()}' if custom_field else ''
                if custom_text == ' True':
                    custom_text = ''

                yes_or_no = None

                field_label_with_no_dashed = [
                    'No significant medical history'
                ]

                fields_list_with_yes_no = [
                    'female_hirsuitism_year', 'female_anti_phospholipid_syndrome_date',
                    'female_blood_transfusion_date',
                    'male_anti_phospholipid_syndrome_date', 'male_blood_transfusion_date',
                    'male_hirsuitism_year'
                ]
                ''' Please populate this for every key which is not object '''
                fields_list_without_year = [
                    'female_no_medical_history', 'male_no_medical_history',
                    'male_att_months', 'female_att_months',
                    'female_hirsuitism', 'male_hirsuitism',
                    'female_hirsuitism_treatment', 'male_hirsuitism_treatment',
                    'female_medical_current_medication', 'male_medical_current_medication',
                    'female_medical_current_allergies', 'male_medical_current_allergies',
                    'female_weight_at_marriage', 'male_weight_at_marriage',
                    'female_weight_comments', 'male_weight_comments',
                    'female_diabetes_type', 'male_diabetes_type',
                    'female_thyroid_type', 'male_thyroid_type',
                ]

                if field_name not in fields_list_without_year:
                    if field_name in fields_list_with_yes_no:
                        field_name = field_name.replace('_year', '').replace('_date', '')
                        yes_or_no = getattr(medical_history, field_name, None)
                        if yes_or_no:
                            custom_text = yes_or_no + ' - ' + custom_text
                        medical_history_year = field_records.year
                    else:
                        medical_history_year = field_records.year
                else:
                    medical_history_year = None

                year_in_bracket = f" ({medical_history_year})" if medical_history_year else ""

                if field_label and field_label in field_label_with_no_dashed:
                    field_text = f'<strong style="font-weight: 700;">{field_label}</strong>'
                else:
                    field_text = f'<strong style="font-weight: 700;">{field_label}</strong><br>{custom_text}{year_in_bracket}'
                medical_history_text.append(field_text)

        if medical_history_text:
            medical_history_text = '<br>'.join(medical_history_text)
            return medical_history_text

        return None

    ''' Computed methods '''

    @api.onchange('create_date_first_consultation')
    def ec_create_date_first_consultation(self):
        if self:
            for record in self:
                if record.create_date_first_consultation:
                    if CustomDateTime.datetime_greater_than_today(record.create_date_first_consultation):
                        record.create_date_first_consultation = None
                        raise ValidationError(_(
                            "Date/Time can't be greater than current date time!"))
                    record.ec_create_date_first_consultation_computed = record.create_date_first_consultation
                else:
                    record.ec_create_date_first_consultation_computed = None

    @api.onchange('repeat_date', 'lmp_question_four')
    def _compute_cycle_day(self):
        """
        This is the onchange on the repeat consultation form.
        Formula: (Consultation Date - LMP) + 1
        :return: cycle day
        """
        if self.repeat_date:
            if CustomDateTime.datetime_greater_than_today(self.repeat_date):
                self.repeat_date = None
                raise ValidationError(_(
                    "Date can't be greater than current date!"))
        if self.lmp_question_four:
            if CustomDateTime.greater_than_today(self.lmp_question_four):
                self.lmp_question_four = None
                raise ValidationError(_(
                    "Date can't be greater than current date!"))

            if self.lmp_question_four and self.repeat_date:
                if self.lmp_question_four > self.repeat_date.date():
                    raise ValidationError(_(
                        "LMP Date can't be greater than current consultation date!"))

            cycle_day = (self.repeat_date.date() - self.lmp_question_four).days
            cycle_day += 1

            self.repeat_cycle_day = cycle_day
            self.tvs_cycle_day = cycle_day
        else:
            self.repeat_cycle_day = 0
            self.tvs_cycle_day = 0

    @api.onchange('create_date_first_consultation', 'gynaecological_examination_lmp')
    def _compute_gynaecological_examination_cycle_day(self):
        """
        This is the onchange on the first consultation form.
        Formula: (Consultation Date - LMP) + 1
        :return: cycle day
        """
        if self.gynaecological_examination_lmp:
            if CustomDateTime.greater_than_today(self.gynaecological_examination_lmp):
                self.gynaecological_examination_lmp = None
                raise ValidationError(_(
                    "Date can't be greater than current date!"))

            if self.gynaecological_examination_lmp and self.create_date_first_consultation:
                if self.gynaecological_examination_lmp > self.create_date_first_consultation.date():
                    raise ValidationError(_(
                        "LMP Date can't be greater than current consultation date!"))

            cycle_day = (self.create_date_first_consultation.date() - self.gynaecological_examination_lmp).days
            cycle_day += 1

            self.gynaecological_examination_cycle_day = cycle_day
        else:
            self.gynaecological_examination_cycle_day = 0

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
        count_after_24_weeks = 0  # Or parity
        for obs_history in obs_histories:
            dop = obs_history.duration_of_pregnancy.replace("<", "").replace(">", "") \
                if obs_history.duration_of_pregnancy else None

            if dop:
                dop = int(dop)

                if dop >= 24:
                    count_after_24_weeks += 1
                # if dop < 24 and obs_history.mode_of_delivery == 'MISCARRIAGE':
                # before it was logic which then excluded the Miscarriages
                if dop < 24:
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
            'male_twins_ids': ('Multiple Pregnancies', 'male_other_twins'),
            'male_tuberculosis_ids': ('Tuberculosis', 'male_other_tuberculosis'),
            'male_abnormalities_ids': ('Congenital Abnormalities', 'male_other_abnormalities'),
            'male_heart_disease_ids': ('Heart Disease', 'male_other_heart_disease'),
            'male_subfertility_ids': ('Subfertility', 'male_other_subfertility'),
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
            'female_heart_disease_ids': ('Heart Disease', 'female_other_heart_disease'),
            'female_subfertility_ids': ('Subfertility', 'female_other_subfertility'),
            'female_twins_ids': ('Multiple Pregnancies', 'female_other_twins'),
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

    def _compute_medical_history(self):
        # Male Fields Processing

        male_fields_to_process = {
            'male_no_medical_history': ('No significant medical history', 'male_no_medical_history'),
            'male_acne_date': ('Acne', 'male_acne'),
            'male_weight_gain_year': ('Weight gain', 'male_weight_gain'),
            'male_weight_loss_year': ('Weight loss', 'male_weight_loss'),
            'male_weight_at_marriage': ('Weight at marriage', 'male_weight_at_marriage'),
            'male_weight_comments': ('Comments', 'male_weight_comments'),
            'male_hirsuitism_year': ('Hirsuitism', 'male_hirsuitism_comments'),
            'male_hirsuitism_treatment': ('Any treatment', 'male_hirsuitism_treatment'),
            'male_tuberculosis_date': ('Tuberculosis', 'male_tuberculosis'),
            'male_att_months': ('ATT (Months)', 'male_att_months'),
            'male_syphilis_date': ('Syphilis', 'male_syphilis'),
            'male_herpes_date': ('Herpes', 'male_herpes'),
            'male_gonorrhoea_date': ('Gonorrhoea', 'male_gonorrhoea'),
            'male_hiv_date': ('HIV', 'male_hiv'),
            'male_mumps_date': ('Mumps', 'male_mumps'),
            'male_adrenal_date': ('Adrenal', 'male_adrenal'),
            'male_anti_phospholipid_syndrome_date': ('Anti-phospholipid Syndrome',
                                                     'male_anti_phospholipid_syndrome_comments'),
            'male_autoimmune_disease_date': ('Autoimmune Diseases', 'male_autoimmune_disease'),
            'male_blood_transfusion_date': ('Blood Transfusion', 'male_blood_transfusion_comments'),
            'male_cardiac_date': ('Cardiac', 'male_cardiac'),
            'male_diabetes_type': ('Diabetes Type', 'male_diabetes_type'),
            'male_diabetes_date': ('Diabetes', 'male_diabetes'),
            'male_gall_bladder_date': ('Gall Bladder', 'male_gall_bladder'),
            'male_gastric_date': ('Gastric', 'male_gastric'),
            'male_gynaecology_date': ('Gynecological', 'male_gynaecology'),
            'male_haematology_date': ('Haematological', 'male_haematology'),
            'male_intestinal_date': ('Intestinal', 'male_intestinal'),
            'male_liver_date': ('Liver', 'male_liver'),
            'male_low_urinary_tract_date': ('Lower Urinary Tract', 'male_low_urinary_tract'),
            'male_malignancy_date': ('Malignancies', 'male_malignancy'),
            'male_neurological_date': ('Neurological', 'male_neurological'),
            'male_renal_date': ('Renal', 'male_renal'),
            'male_respiratory_date': ('Respiratory', 'male_respiratory'),
            'male_skeletal_date': ('Skeletal', 'male_skeletal'),
            'male_thyroid_type': ('Thyroid Type', 'male_thyroid_type'),
            'male_thyroid_date': ('Thyroid', 'male_thyroid_medical'),
            'male_heart_disease_date': ('Heart Disease', 'male_heart_disease'),
            'male_urinary_infection_date': ('Urinary Infections', 'male_urinary_infection'),
            'male_hyper_tension_date': ('Hypertension Pr', 'male_hyper_tension'),
            'male_janduice_date': ('Jaundice', 'male_janduice'),
            'male_complications_pr': ('Complications', 'male_complications_pr'),
            'male_dvt_date': ('DVT', 'male_dvt'),
            'male_smoking_date': ('Smoking', 'male_smoking'),
            'male_alcohol_date': ('Alcohol', 'male_alcohol'),
            'male_medical_history_others_date': ('Others', 'male_medical_history_others'),
            'male_medical_current_medication': ('Current Medication ', 'male_medical_current_medication'),
            'male_medical_current_allergies': ('Allergies', 'male_medical_current_allergies'),
        }

        # if self.male_no_medical_history is False:
        self.male_medical_history = PatientTimeline._compute_patient_medical_history(
            medical_history=self.ec_first_consultation_id.ec_male_medical_history_id,
            fields_to_process=male_fields_to_process
        )
        # else:
        #     self.male_medical_history = None

        # Female Fields Processing

        female_fields_to_process = {
            'female_no_medical_history': ('No significant medical history', 'female_no_medical_history'),
            'female_acne_date': ('Acne', 'female_acne'),
            'female_weight_gain_year': ('Weight gain', 'female_weight_gain'),
            'female_weight_loss_year': ('Weight loss', 'female_weight_loss'),
            'female_weight_at_marriage': ('Weight at marriage', 'female_weight_at_marriage'),
            'female_weight_comments': ('Comments', 'female_weight_comments'),
            'female_hirsuitism_year': ('Hirsuitism', 'female_hirsuitism_comments'),
            'female_hirsuitism_treatment': ('Any treatment', 'female_hirsuitism_treatment'),
            'female_tuberculosis_date': ('Tuberculosis', 'female_tuberculosis'),
            'female_att_months': ('ATT (Months)', 'female_att_months'),
            'female_syphilis_date': ('Syphilis', 'female_syphilis'),
            'female_herpes_date': ('Herpes', 'female_herpes'),
            'female_gonorrhoea_date': ('Gonorrhoea', 'female_gonorrhoea'),
            'female_hiv_date': ('HIV', 'female_hiv'),
            'female_mumps_date': ('Mumps', 'female_mumps'),
            'female_adrenal_date': ('Adrenal', 'female_adrenal'),
            'female_anti_phospholipid_syndrome_date': (
                'Anti-phospholipid Syndrome', 'female_anti_phospholipid_syndrome_comments'),
            'female_autoimmune_disease_date': ('Autoimmune Diseases', 'female_autoimmune_disease'),
            'female_blood_transfusion_date': ('Blood Transfusion', 'female_blood_transfusion_comments'),
            'female_cardiac_date': ('Cardiac', 'female_cardiac'),
            'female_diabetes_type': ('Diabetes Type', 'female_diabetes_type'),
            'female_diabetes_date': ('Diabetes', 'female_diabetes'),
            'female_gall_bladder_date': ('Gall Bladder', 'female_gall_bladder'),
            'female_gastric_date': ('Gastric', 'female_gastric'),
            'female_gynaecology_date': ('Gynecological', 'female_gynaecology'),
            'female_haematology_date': ('Haematological', 'female_haematology'),
            'female_intestinal_date': ('Intestinal', 'female_intestinal'),
            'female_liver_date': ('Liver', 'female_liver'),
            'female_low_urinary_tract_date': ('Lower Urinary Tract', 'female_low_urinary_tract'),
            'female_malignancy_date': ('Malignancies', 'female_malignancy'),
            'female_neurological_date': ('Neurological', 'female_neurological'),
            'female_renal_date': ('Renal', 'female_renal'),
            'female_respiratory_date': ('Respiratory', 'female_respiratory'),
            'female_skeletal_date': ('Skeletal', 'female_skeletal'),
            'female_thyroid_type': ('Thyroid Type', 'female_thyroid_type'),
            'female_thyroid_date': ('Thyroid', 'female_thyroid_medical'),
            'female_heart_disease_date': ('Heart Disease', 'female_heart_disease'),
            'female_urinary_infection_date': ('Urinary Infections', 'female_urinary_infection'),
            'female_hyper_tension_date': ('Hypertension Pr', 'female_hyper_tension'),
            'female_janduice_date': ('Jaundice', 'female_janduice'),
            'female_complications_pr': ('Complications', 'female_complications_pr'),
            'female_dvt_date': ('DVT', 'female_dvt'),
            'female_smoking_date': ('Smoking', 'female_smoking'),
            'female_alcohol_date': ('Alcohol', 'female_alcohol'),
            'female_medical_history_others_date': ('Others', 'female_medical_history_others'),
            'female_medical_current_medication': ('Current Medication', 'female_medical_current_medication'),
            'female_medical_current_allergies': ('Allergies', 'female_medical_current_allergies'),
        }
        # if self.female_no_medical_history is False:
        self.female_medical_history = PatientTimeline._compute_patient_medical_history(
            medical_history=self.ec_first_consultation_id.ec_female_medical_history_id,
            fields_to_process=female_fields_to_process
        )
        # else:
        #     self.female_medical_history = None

    def _compute_surgical_history(self):
        # Male Fields Processing
        for record in self:
            html_content = ""
            for surgery in record.ec_first_consultation_id.male_procedures_ids:
                type_of_surgery_label = dict(
                    self.env['ec.patient.procedures']._fields['type_of_surgery'].selection).get(surgery.type_of_surgery,
                                                                                                '')
                field_text = (f'<p> {surgery.details} ({surgery.surgical_year_id.year})'
                              f'</p<br>')
                html_content += field_text
            record.male_surgical_history = html_content
        # Male Fields Processing

        for record in self:
            html_content = ""
            for surgery in record.ec_first_consultation_id.female_procedures_ids:
                type_of_surgery_label = dict(
                    self.env['ec.patient.procedures']._fields['type_of_surgery'].selection).get(surgery.type_of_surgery,
                                                                                                '')
                field_text = (f'<p> {surgery.details} ({surgery.surgical_year_id.year})'
                              f'</p>')
                html_content += field_text
            record.female_surgical_history = html_content

    def _compute_infertility_type(self):
        for record in self:
            if len(record.first_obs_history_ids) > 0:
                record.infertility_type = StaticMember.INFERTILITY[1][1]
            else:
                record.infertility_type = StaticMember.INFERTILITY[0][1]

    ''' Override methods '''

    def write(self, vals_list):
        record = super(PatientTimeline, self).write(vals_list)
        return record

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
        # if not self.env.user.has_group('ecare_medical_history.group_medical_history_timeline_edit'):
        #     raise UserError("Logged in user does not have the access to perform this action.")
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

    def action_open_patient_semen_view(self):
        patient_id = self.env.context.get('0')
        if patient_id:
            context = {
                'default_semen_patient_id': patient_id,
            }
            domain = [
                ('semen_patient_id', '=', patient_id),
            ]
            return {
                "name": _("Semen Analysis"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.semen.analysis',
                'view_id': self.env.ref('ecare_medical_history.ec_semen_analysis_tree_read_only_view').id,
                'view_mode': 'tree',
                "target": 'main',
                'context': context,
                'domain': domain,
            }
        else:
            raise UserError("Patient does not have any semen record.")

    def action_open_patient_timeline_view(self):
        patient_id = self.env.context.get('0')
        if patient_id:
            timeline_exists = self.env['ec.patient.timeline'].search([('timeline_patient_id', '=', int(patient_id))])

            return {
                "name": _("Timeline"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.patient.timeline',
                'view_id': self.env.ref('ecare_medical_history.patient_timeline_form_view').id,
                'view_mode': 'form',
                "target": 'main',
                'res_id': timeline_exists.id,
            }
        else:
            raise UserError("Patient does not have any record.")

    def action_decision_open_patient_timeline_view(self):
        patient_id = self.timeline_patient_id.id
        if patient_id:
            timeline_exists = self.env['ec.patient.timeline'].search([('timeline_patient_id', '=', int(patient_id))])

            return {
                "name": _("Timeline"),
                "type": 'ir.actions.act_window',
                "res_model": 'ec.patient.timeline',
                'view_id': self.env.ref('ecare_medical_history.patient_timeline_form_view').id,
                'view_mode': 'form',
                "target": 'main',
                'res_id': timeline_exists.id,
            }
        else:
            raise UserError("Patient does not have any record.")

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
                self.ec_repeat_consultation_id.action_set_post_required_attributes()  # Need to call this explicitly here.
            return

        repeat_consultation_id = self.env['ec.repeat.consultation'].create(
            self._get_repeat_consultation_mandatory_attribute()
        )

        self.ec_repeat_consultation_id = repeat_consultation_id.id
        self.ec_repeat_consultation_id.action_set_post_required_attributes()

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

    def action_open_gynae_scan(self):
        return self.ec_first_consultation_id.ec_medical_gynaecological_examination_id.action_open_gynae_scan()

    ''' Data methods '''

    def _get_repeat_consultation_mandatory_attribute(self):
        patient_id = self.timeline_patient_id.id
        repeat_obs_history_lines = len(self.repeat_obs_history_ids.ids)
        repeat_previous_treatment_lines = len(self.timeline_previous_treatment_ids.ids)
        return {
            'repeat_timeline_id': self.id,
            'repeat_patient_id': patient_id,
            'tvs_patient_id': patient_id,
            'tvs_repeat_consultation_id': self.ec_repeat_consultation_id.id,
            'repeat_obs_history_lines': int(repeat_obs_history_lines),
            'repeat_previous_treatment_lines': int(repeat_previous_treatment_lines)
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
        # if ((self.ec_repeat_consultation_id.question_one_choice == 'no') and
        #         (not self.ec_repeat_consultation_id.repeat_diagnosis
        #         or not self.ec_repeat_consultation_id.repeat_procedure_recommended_ids)):
        #     raise ValidationError('Diagnosis and Procedure Recommended can not be empty.')
        # else:
        # if ((self.ec_repeat_consultation_id.question_two_choice == 'yes' and
        #      self.ec_repeat_consultation_id.repeat_obs_history_lines >= len(self.repeat_obs_history_ids.ids)) or
        #         (self.ec_repeat_consultation_id.question_three_choice == 'yes' and
        #          self.ec_repeat_consultation_id.repeat_previous_treatment_lines >=
        #          len(self.timeline_previous_treatment_ids.ids))):
        if self.ec_repeat_consultation_id.question_two_choice == 'yes':
            current_repeat_date = self.ec_repeat_consultation_id.repeat_date
            obstetrics_records = self.repeat_obs_history_ids
            if obstetrics_records:
                records_after_repeat_date = [record for record in obstetrics_records if
                                             record.create_date > current_repeat_date]
                if not records_after_repeat_date:
                    raise ValidationError("Once the question two is answered as 'Yes' "
                                          "then new record in Pregnancy table must be added.")
        if self.ec_repeat_consultation_id.question_three_choice == 'yes':
            current_repeat_date = self.ec_repeat_consultation_id.repeat_date
            treatment_line_records = self.timeline_previous_treatment_ids
            if treatment_line_records:
                records_after_repeat_date = [record for record in treatment_line_records if
                                             record.create_date > current_repeat_date]
                if not records_after_repeat_date:
                    raise ValidationError("If the question three is answered as 'Yes' "
                                          "then new record must be added in the Treatment table.")

        self.show_repeat_section_state = False
        self.ec_repeat_consultation_id.repeat_consultation_state = 'closed'

    def action_delete_repeat_consultation_section(self):
        return self.ec_repeat_consultation_id.action_delete_repeat_consultation_section(self)

    @api.onchange('female_lmp')
    def _check_female_lmp_date(self):
        if self.female_lmp:
            return Validation._date_validation(self.female_lmp)

    @api.onchange('biological_female_dob')
    def _check_biological_female_dob_date(self):
        if self.biological_female_dob and self.timeline_patient_id.married_since:
            if self.biological_female_dob > self.timeline_patient_id.married_since:
                self.biological_female_dob = None
                return {

                    'warning': {

                        'title': 'Warning!',

                        'message': 'Date of birth should be lesser than date of Marriage.'}

                }
            else:
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
        if (self.female_weight and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_weight) or
                self.female_height and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_height)):
            raise UserError(f"Please enter a numeric value in female weight!")
        if self.female_weight and self.female_height:
            female_height = float(self.female_height)
            female_weight = float(self.female_weight)
            height_in_meters = (female_height / 100)
            female_bmi = female_weight / (height_in_meters ** 2)
            self.female_bmi = round(female_bmi, 2)
        else:
            self.female_bmi = None

    @api.onchange('male_weight', 'male_height')
    def _calculate_physical_exam_male_bmi(self):
        if (self.male_weight and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_weight) or
                self.male_height and not re.match(Validation.REGEX_FLOAT_2_DP, self.male_height)):
            raise UserError(f"Please enter a numeric value in male weight and height!")
        if self.male_weight and self.male_height:
            male_height = float(self.male_height)
            male_weight = float(self.male_weight)
            height_in_meters = (male_height / 100)
            male_bmi = male_weight / (height_in_meters ** 2)
            self.male_bmi = round(male_bmi, 2)
        else:
            self.male_bmi = None

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

    @api.onchange('female_ot_ti_weight', 'female_ot_ti_height')
    def _compute_female_ot_ti_bmi(self):
        for record in self:
            if (record.female_ot_ti_weight and record.female_ot_ti_height and
                    float(record.female_ot_ti_weight) > 0 and float(record.female_ot_ti_height) > 0):
                height_in_meters = float(record.female_ot_ti_height) / 100
                record.female_ot_ti_bmi = round(float(record.female_ot_ti_weight) / (height_in_meters ** 2), 2)
            else:
                record.female_ot_ti_bmi = None

    def check_field_values_as_blue(self):
        yes_values = ['yes']

        if self.menopause_sign_suspicion in yes_values:
            return True
        if self.diagnosis_cervical_incompetence in yes_values:
            return True

        return False

    def action_create_oi_ti_platform_attempt(self):
        oi_ti_platform_attempt_ref = self.env['ec.medical.oi.ti.platform.attempt']
        oi_ti_platform_attempt_ref.create_oi_ti_platform_attempt(self, self.ec_repeat_consultation_id)

    def action_treatment_state_instantiate(self):
        if self:
            self.ec_repeat_consultation_id.action_treatment_state_instantiate()

    def action_proceed_to_ui_ti(self):
        fields = [
            'upt_result',
            'iui_plan',
            # 'primary_indication',
            'fsh_lh_amh_acceptable',
            'menopause_sign_suspicion',
            'female_ot_ti_weight',
            'female_ot_ti_height',
            'female_ot_ti_bmi',
            'tubal_patency_test',
            # 'tubal_patency_test_dropdown',
            'cervical_incompetence_diagnosis',
            'uterine_tubal_anomalies',
            'male_semen_analysis',
            'husband_availability_male',
            # 'frozen_sample_available_male',
            'risk_inability_to_give_samples_male',
            'counselling_multiple_birth',
            'counselling_failure_treatment',
            'counselling_lower_success_rate',
            'counselling_high_bmi',
            # 'oi_ti_treatment_prompt_message',
            # 'oi_ti_additional_comments'
        ]

        for field in fields:
            formatted_field_name = field.replace('_', ' ').title()
            value = getattr(self.ec_repeat_consultation_id, field)
            if value is None or value is False:
                raise UserError(f"Field '{formatted_field_name}' is not set. Please fill it before proceeding.")

        # if self.ec_repeat_consultation_id.treatment_state == 'approval':
        #     field_decision = ['menopause_sign_suspicion_decision',
        #                       'female_ot_ti_bmi_decision',
        #                       'fsh_lh_amh_acceptable_decision',
        #                       'tubal_patency_test_dropdown_decision',
        #                       'cervical_incompetence_diagnosis_decision',
        #                       'uterine_tubal_anomalies_decision',
        #                       'male_semen_analysis_decision',
        #                       'risk_inability_male_decision',
        #                       'counselling_multiple_birth_decision',
        #                       'counselling_failure_treatment_decision',
        #                       'counselling_lower_success_rate_decision',
        #                       'oi_ti_additional_comments',
        #                       'counselling_high_bmi_decision']
        #     for field in field_decision:
        #         formatted_field_name = field.replace('_', ' ').title()
        #         value = getattr(self.ec_repeat_consultation_id, field)
        #         if value is None or value is False:
        #             raise UserError(f"Field '{formatted_field_name}' is not set. Please fill it before proceeding.")

        proceed_to_ui_ti = self.env.context.get('proceed_to_ui_ti')
        repeat_ui_ti_add = self.env.context.get('repeat_ui_ti_add')
        repeat_consultation_id = self.ec_repeat_consultation_id.id
        oi_ti_attempts = self.env['ec.medical.oi.ti.platform.cycle'].search([
            ('repeat_consultation_id', '=', int(repeat_consultation_id))])
        if oi_ti_attempts:
            # if len(oi_ti_attempts) >= 3:
            #     raise UserError("Three attempts against one OI/TI cycle have already been made, "
            #                     "start a new repeat consultation first.")
            for rec in oi_ti_attempts:
                if rec.oi_ti_platform in ['ready_to_trigger', '2nd_trigger', 'luteal_phase']:
                    raise UserError("There is a cycle already in progress, please complete that first!")
        if repeat_ui_ti_add:
            self.oi_ti_platform_enabled = True
            recent_repeat_consultation = self.env['ec.repeat.consultation'].search([
                ('repeat_timeline_id', '=', self.id),
                ('repeat_new_treatment_pathway', '=', 'yes'),
            ], order='write_date desc', limit=1)
            if recent_repeat_consultation:
                oi_ti_cycle = self.env['ec.medical.oi.ti.platform.cycle'].search([
                    ('repeat_consultation_id', '=', int(recent_repeat_consultation.id))])
                if oi_ti_cycle and len(oi_ti_cycle) >= 3:
                    raise UserError("Three attempts against one OI/TI cycle have already been made, "
                                    "start a new repeat consultation first.")
                oi_ti_platform_cycle_ref = self.env['ec.medical.oi.ti.platform.cycle']
                self.ec_repeat_consultation_id.treatment_state = 'treatment_started'
                return oi_ti_platform_cycle_ref.create_oi_ti_platform_cycle(self, self.ec_repeat_consultation_id)

        if proceed_to_ui_ti:
            self.oi_ti_platform_enabled = True
            self.action_save_repeat_consultation_section()
            oi_ti_platform_cycle_ref = self.env['ec.medical.oi.ti.platform.cycle']
            self.ec_repeat_consultation_id.treatment_state = 'treatment_started'
            return oi_ti_platform_cycle_ref.create_oi_ti_platform_cycle(self, self.ec_repeat_consultation_id)
        message = ("One or more contraindications to OI/TI have been identified and highlighted and therefore, "
                   "you cannot authorise OI/TI treatment "
                   "pathway for this couple. Proceeding to OI/TI "
                   "will have either inappropriate or with poor "
                   "prognosis and/or higher risk of complications. "
                   "Please discuss it with your seniors.")
        check_red_values = self.ec_repeat_consultation_id.check_field_values_as_red()
        if check_red_values:
            self.ec_repeat_consultation_id.female_ot_ti_checklist_id.oi_ti_treatment_prompt_message = message
            return self.ec_repeat_consultation_id.action_treatment_state_approval()
            # values = {
            #     'default_message': "One or more contraindications to OI/TI have "
            #                        "been identified and highlighted and therefore, "
            #                        "you cannot authorise OI/TI treatment pathway for this couple. "
            #                        "Proceeding to OI/TI will have either inappropriate or "
            #                        "with poor prognosis and/or higher risk of complications. "
            #                        "Please discuss it with your seniors.",
            #     # 'default_ec_repeat_consultation_id': self.ec_repeat_consultation_id.id,
            # }
            # return {
            #     'name': 'Message',
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'form',
            #     'views': [(False, 'form')],
            #     'res_model': 'ec.medical.treatment.pathway.wizard',
            #     'context': values,
            #     'target': 'new',
            # }
        check_blue_values = self.ec_repeat_consultation_id.check_field_values_as_blue()
        if check_blue_values:
            self.ec_repeat_consultation_id.female_ot_ti_checklist_id.oi_ti_treatment_prompt_message = message
            return self.ec_repeat_consultation_id.action_treatment_state_approval()
            # values = {
            #     'default_message': "One or more contraindications to OI/TI have "
            #                        "been identified and highlighted and therefore, "
            #                        "you cannot authorise OI/TI treatment pathway for this couple. "
            #                        "Proceeding to OI/TI will have either inappropriate or "
            #                        "with poor prognosis and/or higher risk of complications. "
            #                        "Please discuss it with your seniors.",
            #     # 'default_ec_repeat_consultation_id': self.ec_repeat_consultation_id.id,
            # }
            # return {
            #     'name': 'Message',
            #     'type': 'ir.actions.act_window',
            #     'view_mode': 'form',
            #     'views': [(False, 'form')],
            #     'res_model': 'ec.medical.treatment.pathway.wizard',
            #     'context': values,
            #     'target': 'new',
            # }
        if (float(self.fsh_level) > 10 or float(self.lh_level) > 10 or
                not (10 <= float(self.amh_level) <= 25)):
            values = {
                'default_message': "Hormonal Profile values are not in range. "
                                   "Please seek senior doctor's approval.",
                'default_ec_repeat_consultation_id': self.ec_repeat_consultation_id.id,
            }
            return {
                'name': 'Message',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'views': [(False, 'form')],
                'res_model': 'ec.medical.treatment.pathway.wizard',
                'context': values,
                'target': 'new',
            }
            # self.ec_repeat_consultation_id.repeat_consultation_state = 'decision_pending'
            # raise ValidationError(_("Hormonal Profile values are not in range. "
            #                         "Please seek senior doctor's approval."))

        self.oi_ti_platform_enabled = True
        self.action_save_repeat_consultation_section()
        oi_ti_platform_cycle_ref = self.env['ec.medical.oi.ti.platform.cycle']
        self.ec_repeat_consultation_id.treatment_state = 'treatment_started'
        return oi_ti_platform_cycle_ref.create_oi_ti_platform_cycle(self, self.ec_repeat_consultation_id)
        # message = "Repeat consultation is closed and entry in OVA platform is added."

    def action_not_proceed_to_ui_ti(self):
        self.ec_repeat_consultation_id.repeat_consultation_state = 'closed'
        self.show_repeat_section_state = False
        record_male = self.env.ref('ecare_medical_history.unsuitable_male', raise_if_not_found=False)
        record_female = self.env.ref('ecare_medical_history.unsuitable_female', raise_if_not_found=False)
        if record_female:
            if record_female not in self.female_factor_ids:
                self.female_factor_ids |= record_female
        if record_male:
            if record_male not in self.male_factor_ids:
                self.male_factor_ids |= record_male
        else:
            print("Record not found")

    @api.onchange('repeat_pregnancy_temp')
    def _check_float_input_temp(self):
        if self.repeat_pregnancy_temp and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_temp):
            raise UserError(f"Please enter a numeric value in pregnancy temperature.")

    @api.onchange('lining_size_decimal')
    def _check_float_input_lining_size(self):
        if self.lining_size_decimal and not re.match(Validation.REGEX_FLOAT_2_DP, self.lining_size_decimal):
            raise UserError(f"Please enter a numeric value in CET.")

    @api.onchange('tvs_lining_size_decimal')
    def _check_float_tvs_lining_size(self):
        if self.tvs_lining_size_decimal and not re.match(Validation.REGEX_FLOAT_2_DP, self.tvs_lining_size_decimal):
            raise UserError(f"Please enter a numeric value in CET.")

    @api.onchange('repeat_pregnancy_hr')
    def _check_float_input_hr(self):
        if self.repeat_pregnancy_hr and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_hr):
            raise UserError(f"Please enter a numeric value in pregnancy HR.")

    @api.onchange('repeat_pregnancy_bp_upper')
    def _check_float_input_bp_upper(self):
        if self.repeat_pregnancy_bp_upper and not re.match(Validation.REGEX_INTEGER_SIMPLE,
                                                           self.repeat_pregnancy_bp_upper):
            raise UserError(f"Please enter a numeric value in pregnancy BP (Upper).")

    @api.onchange('repeat_pregnancy_bp_lower')
    def _check_float_input_bp_lower(self):
        if self.repeat_pregnancy_bp_lower and not re.match(Validation.REGEX_INTEGER_SIMPLE,
                                                           self.repeat_pregnancy_bp_lower):
            raise UserError(f"Please enter a numeric value in pregnancy BP (Lower).")

    @api.onchange('repeat_pregnancy_rr')
    def _check_float_input_rr(self):
        if self.repeat_pregnancy_rr and not re.match(Validation.REGEX_FLOAT_2_DP, self.repeat_pregnancy_rr):
            raise UserError(f"Please enter a numeric value in pregnancy RR.")

    @api.onchange('repeat_pregnancy_embryos_replaced')
    def _check_input_repeat_pregnancy_embryos_replaced(self):
        if self.repeat_pregnancy_embryos_replaced and not re.match(Validation.REGEX_FLOAT_2_DP,
                                                                   self.repeat_pregnancy_embryos_replaced):
            raise UserError(f"Please enter a numeric value in pregnancy embryos replaced!")

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

    @api.onchange('fsh_level')
    def _check_input_fsh_level(self):
        if self.fsh_level and not re.match(Validation.REGEX_FLOAT_2_DP, self.fsh_level) or float(self.fsh_level) < 0:
            raise UserError(f"Please enter a numeric value in FSH and should be greater than 0!")

    @api.onchange('lh_level')
    def _check_input_lh_level(self):
        if self.lh_level and not re.match(Validation.REGEX_FLOAT_2_DP, self.lh_level) or float(self.lh_level) < 0:
            raise UserError(f"Please enter a numeric value in LH and should be greater than 0!")

    @api.onchange('amh_level')
    def _check_input_amh_level(self):
        if self.amh_level and not re.match(Validation.REGEX_FLOAT_2_DP, self.amh_level) or float(self.amh_level) < 0:
            raise UserError(f"Please enter a numeric value in AMH and should be greater than 0!")

    # female_ot_ti_weight = fields.Char('Weight (kg)')
    # female_ot_ti_height = fields.Char('Height (cm)')
    #
    # female_ot_ti_bmi = fields.Char(string='BMI Calculation')

    @api.onchange('female_ot_ti_weight')
    def _check_input_female_ot_ti_weight(self):
        if (self.female_ot_ti_weight and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_ot_ti_weight) or
                float(self.female_ot_ti_weight) < 0):
            raise UserError(f"Please enter a numeric value in Weight and should be greater than 0!")

    @api.onchange('female_ot_ti_height')
    def _check_input_female_ot_ti_height(self):
        if (self.female_ot_ti_height and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_ot_ti_height) or
                float(self.female_ot_ti_height) < 0):
            raise UserError(f"Please enter a numeric value in Height and should be greater than 0!")

    @api.onchange('female_ot_ti_bmi')
    def _check_input_female_ot_ti_bmi(self):
        if self.female_ot_ti_bmi and not re.match(Validation.REGEX_FLOAT_2_DP, self.female_ot_ti_bmi):
            if float(self.female_ot_ti_bmi) < 0:
                raise UserError(f"Please enter a numeric value in BMI and should be greater than 0!")

    @api.onchange('biological_female_dob_check', 'biological_male_dob_check')
    def _check_same_as_above_functionality(self):
        if self.biological_female_dob_check:
            self.biological_female_dob = None
        if self.biological_male_dob_check:
            self.biological_male_dob = None

    @api.onchange('tubal_patency_test_decision', 'tubal_patency_test_decision',
                  'uterine_tubal_anomalies_decision', 'male_semen_analysis_decision',
                  'counselling_multiple_birth_decision', 'counselling_failure_treatment_decision',
                  'counselling_lower_success_rate_decision', 'counselling_high_bmi_decision',
                  'diagnosis_cervical_incompetence_decision', 'menopause_sign_suspicion_decision',
                  'female_ot_ti_bmi_decision')
    def _compute_decisions_fields(self):
        field_values = [
            self.tubal_patency_test_decision,
            self.tubal_patency_test_decision,
            self.uterine_tubal_anomalies_decision,
            self.male_semen_analysis_decision,
            self.counselling_multiple_birth_decision,
            self.counselling_failure_treatment_decision,
            self.counselling_lower_success_rate_decision,
            self.counselling_high_bmi_decision,
            self.diagnosis_cervical_incompetence_decision,
            self.menopause_sign_suspicion_decision,
            self.female_ot_ti_bmi_decision
        ]

        concatenated_values = '\n'.join(str(value) for value in field_values if value)

        self.oi_ti_decisions = concatenated_values

    @api.onchange('menopause_sign_suspicion_decision',
                  'female_ot_ti_bmi_decision',
                  'fsh_lh_amh_acceptable_decision',
                  'tubal_patency_test_dropdown_decision',
                  'cervical_incompetence_diagnosis_decision',
                  'uterine_tubal_anomalies_decision',
                  'male_semen_analysis_decision',
                  'risk_inability_male_decision',
                  'counselling_multiple_birth_decision',
                  'counselling_failure_treatment_decision',
                  'counselling_lower_success_rate_decision',
                  'counselling_high_bmi_decision')
    def onchange_decision_fields(self):
        # Check if the current user has the role of senior_doctor
        if not self.env.user.has_group('ecare_medical_history.group_ec_medical_senior_doctor'):
            raise UserError("Logged in user does not have the access to change decision fields.")
