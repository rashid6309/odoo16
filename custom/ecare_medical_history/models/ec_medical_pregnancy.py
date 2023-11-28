from odoo import api, fields, models
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember


class PregnancyForm(models.Model):
    _name = 'ec.medical.pregnancy.data'
    _description = 'Pregnancy Data'

    pregnancy_repeat_consultation_id = fields.Many2one(comodel_name='ec.repeat.consultation',
                                                       readonly=True,
                                                       string='Repeat Consultation')

    repeat_pregnancy_lmp = fields.Date(string='LMP')
    repeat_pregnancy_gestational_age = fields.Selection(selection=StaticMember.AGE_WEEKS,
                                                        string="Gestational Age", compute='_compute_gestational_age')

    repeat_pregnancy_conception = fields.Selection(selection=StaticMember.CONCEPTION_TYPE,
                                                   string='Conception')
    repeat_pregnancy_embryos_replaced = fields.Integer(string="In case of IVF/ICSI; number of embryos replaced: ")

    repeat_pregnancy_gestation_type = fields.Selection(StaticMember.GESTATION_TYPE, string="Type of Gestation")
    repeat_pregnancy_other_info = fields.Char(string="Other")

    repeat_pregnancy_viability_potential = fields.Selection(StaticMember.VIABILITY_POTENTIAL, string="Viability Potential")
    repeat_pregnancy_details = fields.Char(string="Details")
    repeat_pregnancy_diagnosis = fields.Char(string="Any significant pregnancy diagnosis?")

    repeat_pregnancy_procedure_performed = fields.Many2one(comodel_name='ec.medical.pregnancy.procedure',
                                                           string="Procedure Performed")
    repeat_pregnancy_procedure_performed_text = fields.Text(string="Procedure Notes")

    repeat_pregnancy_diagnosis_ids = fields.Many2many(comodel_name='ec.medical.diagnosis',
                                                      relation="ec_medical_pregnancy_diagnosis_rel",
                                                      column1="medical_pregnancy_id",
                                                      column2="diagnosis_id",
                                                      string="Diagnosis")

    repeat_pregnancy_diagnosis_id_text = fields.Char(string="Other Diagnosis")

    repeat_pregnancy_investigation_ids = fields.Many2many(comodel_name='ec.medical.investigation',
                                                          relation="ec_medical_pregnancy_investigation_rel",
                                                          column1="medical_pregnancy_id",
                                                          column2="investigation_id",
                                                          string="Investigation")
    repeat_pregnancy_investigation_id_text = fields.Char(string="Investigation Notes")

    repeat_pregnancy_type_sample_obtained = fields.Char(string="Type of Sample Obtained")

    repeat_pregnancy_reason_to_visit = fields.Selection(StaticMember.VISIT_REASON, string="Reason for visit")
    repeat_pregnancy_notes = fields.Char(string="Notes")
    genetic_testing = fields.Char(string="Genetic Testing")
    early_pregnancy_assessment = fields.Char(string="Early Pregnancy Assessment")

    repeat_pregnancy_scanned = fields.Selection(StaticMember.CHOICE_YES_NO, string="Documented Medicsi Scan Reviewed?")
    repeat_pregnancy_significant_findings = fields.Char(string="Mention any SIGNIFICANT findings")

    repeat_pregnancy_hr = fields.Selection(StaticMember.HR_TYPE, string="HR")
    repeat_pregnancy_bp_upper = fields.Integer(string="BP")
    repeat_pregnancy_bp_lower = fields.Integer(string="BP")
    repeat_pregnancy_temp = fields.Float(string="Temp")
    repeat_pregnancy_rr = fields.Integer(string="RR")

    repeat_pregnancy_fetal_heart = fields.Selection(StaticMember.FETAL_HEART, string="Fetal Heart ")

    repeat_pregnancy_signs_of_ohss = fields.Selection(StaticMember.CHOICE_YES_NO_NA, string="Any signs of OHSS?  ")

    repeat_pregnancy_icsi_ultrasound = fields.Char(string="ICSI Ultrasound")

    repeat_pregnancy_name_receiving_geneticist = fields.Many2one(comodel_name='res.consultant',
                                                                 string="Name of Receiving Geneticist")
    repeat_pregnancy_plan = fields.Char(string="Plan")
    repeat_pregnancy_doctors = fields.Many2many(comodel_name='res.consultant',
                                                column1='pregnancy_id',
                                                column2='doctor_id',
                                                relation='ec_medical_pregnancy_doctors_rel',
                                                string="Doctors")

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


class PregnancyProcedures(models.Model):
    _name = 'ec.medical.pregnancy.procedure'
    _description = 'Pregnancy Procedures'

    name = fields.Char("Name", required=True)
    value = fields.Text("Value")
