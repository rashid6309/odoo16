from datetime import datetime

from odoo import api, models, fields, _
import re
from odoo.addons.ecare_medical_history.utils.validation import Validation
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_core.utilities.helper import TimeValidation, CustomNotification


from odoo.exceptions import UserError


class SemenAnalysis(models.Model):
    _name = 'ec.semen.analysis'
    _description = 'Semen Analysis'
    _rec_name = "semen_patient_id"
    _order = "date desc"

    semen_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                       required=True,
                                       string="Patient")

    date = fields.Date(string='Date', required=True,)
    lab_number = fields.Char(string='Lab Number')
    lab_name = fields.Many2one(comodel_name="ec.medical.labs", string='Lab Name')

    preparation_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                       relation='semen_analysis_multi_selection_complains',
                                       column1='semen_id',
                                       column2='multi_selection_id',
                                       string='Preparation', domain="[('type', '=', 'preparation')]")

    sample_produced_at_lab = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                              string='Sample Produced at Lab')

    repeat_semen_analysis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                             string='Repeat Semen Analysis')
    freezing = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                string='Freezing')

    abstinence = fields.Char(string='Abstinence')
    production_time = fields.Char(string='Production Time')
    analysis_time = fields.Char(string='Analysis Time')
    liquifaction_time = fields.Char(string='Liquefaction Time')
    color = fields.Selection(selection=StaticMember.SEMEN_COLOR,
                             string="Color")

    ph = fields.Char(string='PH')
    viscosity = fields.Selection(selection=StaticMember.SEMEN_VISCOSITY, string='Viscosity')
    volume = fields.Char(string='Volume')
    total_count = fields.Char(string='Total Count')
    motility = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Motility')

    progression_f_forward = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='F Forward')
    progression_s_forward = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='S Forward')
    progression_lateral = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Lateral')
    progression_non_progressive = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Non Progressive')
    progression_dead = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Dead')

    # progression = fields.Selection([
    #     ('no_progression', 'No Progression'),
    #     ('limited_progression', 'Limited Progression'),
    #     ('good_progression', 'Good Progression'),
    # ], string='Progression')

    wbcs = fields.Char(string='WBCs')
    agglutination = fields.Selection(selection=StaticMember.SEMEN_SIGN_VALUES, string='Agglutination')
    debris = fields.Selection(selection=StaticMember.SEMEN_SIGN_VALUES, string='Debris')
    bacteria = fields.Selection(selection=StaticMember.SEMEN_SIGN_VALUES, string='Bacteria')
    epi_cells_immature_cells = fields.Char(string='EPI Cells/Immature Cells')
    other_observation = fields.Text(string='Other Observation')

    normal = fields.Selection(selection=StaticMember.SEMEN_MORPHOLOGY, string="Normal")
    abnormal = fields.Selection(selection=StaticMember.SEMEN_MORPHOLOGY, string="Abnormal")

    # Defects
    cephalic = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Cephalic')
    mid_piece = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Mid Piece')
    tail = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Tail')
    acrosomal_cap = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Acrosomal Cap')
    vacoules = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='Vacoules')

    method = fields.Selection(selection=StaticMember.SEMEN_METHOD, string="Method")
    prep_conc = fields.Char(string='Prep Conc')

    motility_percentage = fields.Selection(selection=StaticMember.SEMEN_MOTILITY, string='%Motility')
    progression = fields.Char(string='Progression')

    after_24_hrs_motility_percentage = fields.Selection(selection=StaticMember.SEMEN_MOTILITY,
                                                        string='After 24hrs %Motility')
    after_24_hrs_progression = fields.Char(string='After 24hrs Progression')

    comments = fields.Text(string='Comments')

    # suitable_for

    suitable_for_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                        relation='semen_analysis_multi_selection_suitable_for_rel',
                                        column1='semen_id',
                                        column2='multi_selection_id',
                                        string='Suitable For', domain="[('type', '=', 'suitable_for')]")

    # sperm_cryopreservation = fields.Char()
    sperm_cryopreservation_recommended = fields.Boolean('Recommended')
    sperm_cryopreservation_consented = fields.Boolean('Cryopreservation Consented')
    sperm_cryopreservation_strawe = fields.Char('Cryopreservation Strawe')
    sperm_cryopreservation_code = fields.Char('Cryopreservation Code')

    seminologist_id = fields.Many2one(comodel_name='res.users', string='Seminologist', default=lambda self: self.env.user)
    legacy_seminologist = fields.Char(string="Legacy System Seminologist", readonly=1)

    special_notes = fields.Char("Special Notes")

    seme_analysis_id_dummy = fields.Many2one('ec.semen.analysis')
    
    all_semen_analysis_ids = fields.One2many('ec.semen.analysis', 'seme_analysis_id_dummy',
                                             compute='get_patient_semen_analysis_records')

    def action_open_form_view(self, patient_id):
        context = {
            'default_semen_patient_id': patient_id.id,
        }
        domain = [
            ('semen_patient_id', '=', patient_id.id),
        ]
        return {
            "name": _("Semen Analysis"),
            "type": 'ir.actions.act_window',
            "res_model": 'ec.semen.analysis',
            'view_id': self.env.ref('ecare_medical_history.ec_semen_analysis_tree_read_only_view').id,
            'view_mode': 'tree',
            "target": 'new',
            'context': context,
            'domain': domain,
        }

    def edit_semen_analysis_record(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'ec.semen.analysis',
            'res_id': self.id,
            'view_mode': 'form',
            "target": "main",
        }

    @api.onchange('semen_patient_id')
    def get_patient_semen_analysis_records(self):
        semen_patient_id = self.semen_patient_id
        if semen_patient_id:
            all_semen_analysis_records = self.env['ec.semen.analysis'].search(
                [('semen_patient_id', '=', semen_patient_id.id)])
            if all_semen_analysis_records:
                self.all_semen_analysis_ids = all_semen_analysis_records
            else:
                self.all_semen_analysis_ids = None

            # Filter out self.id from the list of IDs
            # filtered_ids = [rec.id for rec in all_semen_analysis_records if rec.id != self.id]
            #
            # if filtered_ids:
            #     self.all_semen_analysis_ids = [(6, 0, filtered_ids)]
            # else:
            #     self.all_semen_analysis_ids = None

    def delete_semen_analysis_record(self):
        # Unlink (delete) the records
        self.unlink()

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }

    @api.model_create_multi
    def create(self, vals):
        if vals[0].get('lab_number') in [False, '']:
            vals[0]['lab_number'] = self.env['ir.sequence'].next_by_code('ecare_history.semen.sequence.lab.no') or '/'
        return super(SemenAnalysis, self).create(vals)

    def print_semen_analysis_report(self):
        return self.env.ref('ecare_medical_history.ec_semen_analysis_report').report_action(self)

    def print_patient_report(self):
        return self.env.ref('ecare_medical_history.ec_patient_report').report_action(self)

    @api.onchange('date')
    def _check_semen_date(self):
        if self.date:
            return Validation._date_validation(self.date)

    def _check_numeric_input(self, field_name, value):
        if value and not re.match(Validation.REGEX_FLOAT_2_DP, value):
            raise UserError(f"Please enter a numeric value in {field_name} with up to 2 decimal points.")

    @api.onchange('abstinence')
    def _check_abstinence_input(self):
        self._check_numeric_input('abstinence', self.abstinence)

    @api.onchange('volume')
    def _check_volume_input(self):
        self._check_numeric_input('volume', self.volume)

    @api.onchange('total_count')
    def _check_total_count_input(self):
        self._check_numeric_input('total count', self.total_count)

    @api.onchange('wbcs')
    def _check_wbcs_input(self):
        self._check_numeric_input('WBCs', self.wbcs)

    @api.onchange('epi_cells_immature_cells')
    def _check_epi_cells_immature_cells_input(self):
        self._check_numeric_input('EPI Cells/Immature Cells', self.epi_cells_immature_cells)

    @api.onchange('prep_conc')
    def _check_prep_conc_input(self):
        self._check_numeric_input('Prep Conc', self.prep_conc)

    @api.onchange('sperm_cryopreservation_strawe')
    def _check_sperm_cryopreservation_strawe_input(self):
        self._check_numeric_input('No. of Strawe', self.sperm_cryopreservation_strawe)

    @api.onchange('ph')
    def _check_ph_input(self):
        self._check_numeric_input('PH', self.ph)

    @api.onchange('after_24_hrs_progression')
    def _check_after_24_hrs_progression_input(self):
        self._check_numeric_input('After 24hrs Progression', self.after_24_hrs_progression)

    @api.onchange('progression')
    def _check_progression_input(self):
        self._check_numeric_input('progression', self.progression)

    @api.onchange('production_time', "analysis_time", "liquifaction_time")
    def _onchange_time(self):

        if self.production_time:
            time = TimeValidation.validate_time(self.production_time)

            if not time:
                self.production_time = None
                return CustomNotification.notification_time_validation()
            try:
                parsed_time = datetime.strptime(time, '%H:%M')
                if not 0 <= parsed_time.hour <= 23:
                    raise ValueError()
            except ValueError:
                raise UserError("Invalid time format or hours. Please use HH:MM (24-hour format) with valid hours.")
            self.production_time = time

        if self.analysis_time:
            time = TimeValidation.validate_time(self.analysis_time)
            if not time:
                self.analysis_time = None
                return CustomNotification.notification_time_validation()
            try:
                parsed_time = datetime.strptime(time, '%H:%M')
                if not 0 <= parsed_time.hour <= 23:
                    raise ValueError()
            except ValueError:
                raise UserError("Invalid time format or hours. Please use HH:MM (24-hour format) with valid hours.")
            self.analysis_time = time

        if self.liquifaction_time:
            time = TimeValidation.validate_time(self.liquifaction_time)
            if not time:
                self.liquifaction_time = None
                return CustomNotification.notification_time_validation()
            try:
                parsed_time = datetime.strptime(time, '%H:%M')
                if not 0 <= parsed_time.hour <= 23:
                    raise ValueError()
            except ValueError:
                raise UserError("Invalid time format or hours. Please use HH:MM (24-hour format) with valid hours.")
            self.liquifaction_time = time

