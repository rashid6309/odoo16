from odoo import api, fields, models
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class PregnancyForm(models.Model):
    _name = 'ec.medical.pregnancy.data'
    _description = 'Pregnancy Data'

    pregnancy_repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                                       readonly=True,
                                                       string='Repeat Consultation')

    repeat_pregnancy_lmp = fields.Date(string='LMP')
    repeat_pregnancy_gestational_age = fields.Integer(string="Gestational Age")

    repeat_pregnancy_conception = fields.Selection(selection=StaticMember.CONCEPTION_TYPE,
                                                   string='Conception')

    repeat_pregnancy_gestation_type = fields.Selection(StaticMember.GESTATION_TYPE, string="Type of Gestation")
    repeat_pregnancy_other_info = fields.Char(string="Other")

    repeat_pregnancy_viability_potential = fields.Selection(StaticMember.VIABILITY_POTENTIAL, string="Viability Potential")
    repeat_pregnancy_details = fields.Char(string="Details")
    repeat_pregnancy_diagnosis = fields.Char(string="Any significant pregnancy diagnosis?")

    repeat_pregnancy_reason_to_visit = fields.Selection(StaticMember.VISIT_REASON, string="Reason to visit - ")
    repeat_pregnancy_notes = fields.Char(string="Notes")

    repeat_pregnancy_scanned = fields.Selection(StaticMember.CHOICE_YES_NO, string="Documented Medicsi Scan Reviewd?")
    repeat_pregnancy_significant_findings = fields.Char(string="Mention any SIGNIFICANT findings")

    repeat_pregnancy_hr = fields.Selection(StaticMember.HR_TYPE, string="HR")
    repeat_pregnancy_bp = fields.Integer(string="BP")
    repeat_pregnancy_temp = fields.Integer(string="Temp")
    repeat_pregnancy_rr = fields.Integer(string="RR")

    repeat_pregnancy_fetal_heart = fields.Selection(StaticMember.FETAL_HEART, string="Fetal Heart ")

    repeat_pregnancy_signs_of_ohss= fields.Selection(StaticMember.CHOICE_YES_NO_NA, string="Any signs of OHSS?  ")



