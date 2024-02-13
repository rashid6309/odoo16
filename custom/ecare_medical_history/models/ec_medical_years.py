from odoo import models, api, fields
from odoo.addons.ecare_medical_history.utils.validation import Validation
from odoo.exceptions import AccessError, UserError, ValidationError
import re


class EcMedicalYear(models.Model):
    _name = "ec.medical.year"
    _description = "Year"
    _order = 'year desc'
    _rec_name = "year"

    year = fields.Char('Year', required=True)

    @api.model
    def create_medical_year_record(self):
        current_year = fields.Date.today().year
        year_exists = self.env['ec.medical.year'].search([('year', '=', str(current_year))])

        if not year_exists:
            self.env['ec.medical.year'].create({'year': str(current_year)})

        return True

    @api.onchange('repeat_pregnancy_bp_upper')
    def _check_integer_input_year(self):
        if self.year and not re.match(Validation.REGEX_INTEGER_SIMPLE, self.year):
            raise UserError(f"Please enter a numeric value in Year.")
