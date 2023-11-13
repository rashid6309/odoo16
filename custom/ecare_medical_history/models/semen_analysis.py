from odoo import api, models, fields, _

from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class SemenAnalysis(models.Model):
    _name = 'ec.semen.analysis'
    _description = 'Semen Analysis'
    _rec_id = "semen_patient_id"

    semen_patient_id = fields.Many2one(comodel_name="ec.medical.patient",
                                       string="Patient",
                                       readonly=True)

    date = fields.Date(string='Date')
    lab_number = fields.Char(string='Lab Number')
    lab_name = fields.Char(string='Lab Name')

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
    production_time = fields.Float(string='Production Time')
    analysis_time = fields.Float(string='Analysis Time')
    liquifaction_time = fields.Char(string='Liquifaction Time')
    color = fields.Selection(selection=StaticMember.SEMEN_COLOR,
                             default='a',
                             string="Color")

    ph = fields.Char(string='PH')
    viscosity = fields.Selection(selection=StaticMember.SEMEN_VISCOSITY, string='Viscosity')
    volume = fields.Char(string='Volume')
    total_count = fields.Char(string='Total Count')
    mobility = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Mobility')

    progression_f_forward = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='F Forward')
    progression_s_forward = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='S Forward')
    progression_lateral = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Lateral')
    progression_non_progressive = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Non Progressive')
    progression_dead = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Dead')

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
    cephalic = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Cephalic')
    mid_piece = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Mid Piece')
    tail = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Tail')
    acrosomal_cap = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Acrosomal Cap')
    vacoules = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='Vacoules')

    method = fields.Selection(selection=StaticMember.SEMEN_METHOD, string="Method")
    prep_conc = fields.Char(string='Prep Conc')

    mobility_percentage = fields.Selection(selection=StaticMember.SEMEN_MOBILITY, string='%Mobility')
    progression = fields.Char(string='Progression')

    after_24_hrs_mobility_percentage = fields.Selection(selection=StaticMember.SEMEN_MOBILITY,
                                                        string='After 24hrs %Mobility')
    after_24_hrs_progression = fields.Char(string='After 24hrs Progression')

    comments = fields.Text(string='Comments')

    # suitable_for

    suitable_for_ids = fields.Many2many(comodel_name='ec.medical.multi.selection',
                                        relation='semen_analysis_multi_selection_suitable_for',
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
