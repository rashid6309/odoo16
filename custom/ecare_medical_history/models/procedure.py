from odoo import models, fields, api
from odoo.addons.ecare_medical_history.utils.static_members import StaticMember
from odoo.addons.ecare_medical_history.utils.validation import Validation


class PatientProcedures(models.Model):
    _name = 'ec.patient.procedures'
    _description = 'Patient (Common) Procedures'
    _order = 'create_date desc'

    female_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete='restrict')
    male_consultation_id = fields.Many2one(comodel_name='ec.first.consultation', ondelete="restrict")

    type_of_surgery = fields.Selection(
        selection=StaticMember.SURGERY_TYPES,
        string='Type of Surgery',
    )
    details = fields.Char('Details', required=True)

    surgical_year_id = fields.Many2one(
        comodel_name="ec.medical.year",
        string='Year',
        help='Select a year from the list',
    )
