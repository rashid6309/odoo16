from odoo import models, fields, api
from datetime import datetime

class CalculateSLAHoursRemaining(models.Model):
    _name = 'svs.custom.calculate.sla.hours'
    _description = 'Calculates Hours Remaining SLA'

    def calculate_hours_remaining(self):
        for project in self.env['project.project'].search([('x_sla_hours_started', '=', True)]):
            if project.x_sla_datetime and not project.stage_id.fold:
                # Calculate the date difference in hours between project date and now
                project_date = fields.Datetime.from_string(project.x_sla_datetime)
                current_date = datetime.now()
                date_difference_hours = project.x_sla_hours_left- ((current_date - project_date).total_seconds()/3600)

                # Store the result in the custom field x_sla_hours_remaining as an integer
                project.x_sla_hours_remaining = date_difference_hours