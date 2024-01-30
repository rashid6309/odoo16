from odoo import models, api, fields


class EcMedicalYear(models.Model):
    _name = "ec.medical.year"
    _description = "Year"
    _order = 'year desc'
    _rec_name = "year"

    year = fields.Integer('Year', required=True)

    @api.model
    def create_medical_year_record(self):
        current_year = fields.Date.today().year
        year_exists = self.env['ec.medical.year'].search([('year', '=', current_year)])

        if not year_exists:
            self.env['ec.medical.year'].create({'year': current_year})

        return True