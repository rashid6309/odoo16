from datetime import datetime

from odoo import api, models, fields, _
import re
from odoo.addons.ecare_medical_history.utils.date_validation import DateValidation
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_core.utilities.helper import TimeValidation, CustomNotification


from odoo.exceptions import UserError


class SemenAnalysis(models.Model):
    _name = 'ec.semen.analysis'
    _description = 'Semen Analysis'
    _rec_name = "semen_patient_id"

    semen_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                       required=True,
                                       string="Patient")

    date = fields.Date(string='Date', required=True,)
    lab_number = fields.Char(string='Lab Number', required=True,)
    lab_name = fields.Many2one(comodel_name="ec.medical.labs", string='Lab Name')

    preparation_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                       relation='semen_analysis_multi_selection_complains',
                                       column1='semen_id',
                                       column2='multi_selection_id',
                                       string='Preparation', domain="[('type', '=', 'preparation')]")

    sample_produced_at_lab = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                              default='no',
                                              string='Sample Produced at Lab')

    repeat_semen_analysis = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                             default='no',
                                             string='Repeat Semen Analysis')
    freezing = fields.Selection(selection=StaticMember.CHOICE_YES_NO,
                                default='no',
                                string='Freezing')

    abstinence = fields.Char(string='Abstinence')
    production_time = fields.Char(string='Production Time')
    analysis_time = fields.Char(string='Analysis Time')
    liquifaction_time = fields.Char(string='Liquifaction Time')
    color = fields.Selection(selection=StaticMember.SEMEN_COLOR,
                             default='a',
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
    sperm_cryopreservation_consented = fields.Boolean('Cryopreservation Consented')
    sperm_cryopreservation_strawe = fields.Char('Cryopreservation Strawe')
    sperm_cryopreservation_code = fields.Char('Cryopreservation Code')

    seminologist = fields.Char("Seminologist")
    special_notes = fields.Char("Special Notes")

    def print_semen_analysis_report(self):
        return self.env.ref('ecare_medical_history.ec_semen_analysis_report').report_action(self)

    def print_patient_report(self):
        return self.env.ref('ecare_medical_history.ec_patient_report').report_action(self)

    @api.onchange('date')
    def _check_semen_date(self):
        if self.date:
            return DateValidation._date_validation(self.date)

    @api.onchange('abstinence')
    def _check_abstinence_input(self):
        for record in self:
            if record.abstinence and not re.match('^[0-9\.]*$', record.abstinence):
                raise UserError("Please enter a numeric value in abstinence.")
            
    @api.onchange('volume')
    def _check_volume_input(self):
        for record in self:
             if record.volume and not re.match('^[0-9\.]*$', record.volume):
                raise UserError("Please enter a numeric value in volume.")

    @api.onchange('total_count')
    def _check_total_count_input(self):
        for record in self:
             if record.total_count and not re.match('^[0-9\.]*$', record.total_count):
                raise UserError("Please enter a numeric value in total count.")

    @api.onchange('wbcs')
    def _check_wbcs_input(self):
        for record in self:
             if record.wbcs and not re.match('^[0-9\.]*$', record.wbcs):
                raise UserError("Please enter a numeric value in WBCs.")

    @api.onchange('epi_cells_immature_cells')
    def _check_epi_cells_immature_cells_input(self):
        for record in self:
             if record.epi_cells_immature_cells and not re.match('^[0-9\.]*$', record.epi_cells_immature_cells):
                raise UserError("Please enter a numeric value in EPI Cells/Immature Cells.")

    @api.onchange('prep_conc')
    def _check_prep_conc_input(self):
        for record in self:
             if record.prep_conc and not re.match('^[0-9\.]*$', record.prep_conc):
                raise UserError("Please enter a numeric value in Prep Conc")

    @api.onchange('sperm_cryopreservation_strawe')
    def _check_sperm_cryopreservation_strawe_input(self):
        for record in self:
             if record.sperm_cryopreservation_strawe and not re.match('^[0-9\.]*$', record.sperm_cryopreservation_strawe):
                raise UserError("Please enter a numeric value in No. of Strawe.")

    @api.onchange('ph')
    def _check_ph_input(self):
        for record in self:
             if record.ph and not re.match('^[0-9\.]*$', record.ph):
                raise UserError("Please enter a numeric value PH.")

    @api.onchange('progression')
    def _check_progression_input(self):
        for record in self:
             if record.progression and not re.match('^[0-9\.]*$', record.progression):
                raise UserError("Please enter a numeric value progression.")

    @api.onchange('production_time', "analysis_time","liquifaction_time")
    def _onchange_time(self):

        if self.production_time:
            time = TimeValidation.validate_time(self.production_time)

            if not time:
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
                return CustomNotification.notification_time_validation()
            try:
                parsed_time = datetime.strptime(time, '%H:%M')
                if not 0 <= parsed_time.hour <= 23:
                    raise ValueError()
            except ValueError:
                raise UserError("Invalid time format or hours. Please use HH:MM (24-hour format) with valid hours.")
            self.liquifaction_time = time
