from odoo import models, fields, api, _
from odoo.addons.ecare_core.utilities.helper import TimeValidation


class PatientTimeline(models.Model):
    _name = "ec.patient.timeline"
    _description = "Patient Timeline"
    _rec_name = "timeline_patient_id"

    _sql_constraints = [
        ('timeline_patient_id_unique', 'unique (timeline_patient_id)',
         'Multiple patient timelines cant be created, rather open the existing one!'),
    ]

    _inherits = {
        'ec.first.consultation': 'ec_first_consultation_id',
        'ec.repeat.consultation': 'ec_repeat_consultation_id'
    }

    ec_first_consultation_id = fields.Many2one(comodel_name="ec.first.consultation", ondelete='restrict')
    ec_repeat_consultation_id = fields.Many2one(comodel_name="ec.repeat.consultation", ondelete='cascade')

    ''' Foreign keys '''
    timeline_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                          string="Patient",
                                          index=True)

    # Related Fields which are used for kanban view
    # Related Fields Used for data representation purposes
    timeline_patient_mr_num = fields.Char('MR No.', related="timeline_patient_id.mr_num", store=True)
    timeline_patient_name = fields.Char('Patient Name', related="timeline_patient_id.name", store=True)
    timeline_patient_wife_name = fields.Char('Wife Name', related="timeline_patient_id.wife_name", store=True)
    timeline_patient_husband_name = fields.Char('Husband Name', related="timeline_patient_id.husband_name", store=True)

    timeline_patient_mobile_wife = fields.Char('Mobile Wife', related="timeline_patient_id.mobile_wife", store=True)
    timeline_patient_mobile_husband = fields.Char('Husband Wife', related="timeline_patient_id.mobile_husband", store=True)

    timeline_patient_wife_image = fields.Binary('Patient Wife Image', related="timeline_patient_id.image_1920",
                                                store=True)
    timeline_patient_husband_image = fields.Binary('Patient Husband Image', related="timeline_patient_id.husband_image",
                                                   store=True)

    ''' One2Many'''

    repeat_consultation_ids = fields.One2many(comodel_name="ec.repeat.consultation",
                                              inverse_name="repeat_timeline_id")

    show_repeat_section_state = fields.Boolean(default=False, string='Div State')
    show_repeat_consultation_history_section = fields.Boolean(default=False)

    ''' Computed'''

    gravida = fields.Char(string='Gravida', compute='_compute_female_values')
    parity = fields.Char(string='Parity', compute='_compute_female_values')
    miscarriages = fields.Char(string='Miscarriages', compute='_compute_female_values')

    male_family_history = fields.Char(string='Male Family History', compute='_compute_family_history')
    female_family_history = fields.Char(string='Female Family History', compute='_compute_family_history')

    ''' Override methods '''

    # Female Factor

    female_factor_ids = fields.Many2many('ec.medical.factors',
                                         relation="timeline_female_factor_rel",
                                         column1="timeline_id", column2="female_factor_id",
                                         domain=[('type', 'in', ['female'])])
    male_factor_ids = fields.Many2many('ec.medical.factors',
                                       relation="timeline_male_factor_rel",
                                       column1="timeline_id", column2="male_factor_id",
                                       domain=[('type', 'in', ['male'])])
    @api.model
    def create(self, vals):
        res = super(PatientTimeline, self).create(vals)
        res.ec_repeat_consultation_id.update(
            {'repeat_timeline_id': res.id,
             'repeat_patient_id': res.timeline_patient_id
             }
        )

        return res

    ''' XXX - Override methods - XXX'''

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
                    field_text = f'<strong style="font-weight: 700;">{field_label}:</strong><br>{family_members_list}'
                    family_history_text.append(field_text)
            elif field_records or (custom_field and custom_field.strip()):
                custom_text = f' ({custom_field.strip()})' if custom_field else ''
                family_members_list = [rec.name for rec in field_records]
                if family_members_list:
                    field_text = f'<strong style="font-weight: 700;">{field_label}:</strong><br>{", ".join(family_members_list)}{custom_text}'
                    family_history_text.append(field_text)

        if family_history_text:
            family_history_text = '<br>'.join(family_history_text)
            return family_history_text

        return None

    def _compute_family_history(self):
        # Male Fields Processing

        male_fields_to_process = {
            'male_diabetes_ids': ('Diabetes', 'male_other_diabetes'),
            'male_malignancies_ids': ('Malignancies', 'male_other_malignancies'),
            'male_hypertension_ids': ('Hypertension', 'male_other_hypertension'),
            'male_mental_illness_ids': ('Mental Illness', 'male_other_mental_illness'),
            'male_tuberculosis_ids': ('Tuberculosis', 'male_other_tuberculosis'),
            'male_abnormalities_ids': ('Abnormalities', 'male_other_abnormalities'),
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
            'female_abnormalities_ids': ('Abnormalities', 'female_other_abnormalities'),
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
                                                                       self.ec_first_consultation_id)

    def action_create_repeat_consultation(self):
        self.show_repeat_section_state = True
        if self.show_repeat_consultation_history_section is False:
            self.show_repeat_consultation_history_section = True
            return

        repeat_consultation_id = self.env['ec.repeat.consultation'].create({
            'repeat_timeline_id': self.id,
            'repeat_patient_id': self.timeline_patient_id.id
        })
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
        patient_timeline_id = self.env['ec.patient.timeline'].create(values)
        return patient_timeline_id

    @api.onchange('biological_female_dob')
    def _get_biological_age_female(self):
        for rec in self:
            rec.biological_female_age = TimeValidation.convert_date_to_days_years(rec.biological_female_dob)

    @api.onchange('biological_male_dob')
    def _get_biological_age_male(self):
        for rec in self:
            rec.biological_male_age = TimeValidation.convert_date_to_days_years(rec.biological_male_dob)

    ''' Data methods '''
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
