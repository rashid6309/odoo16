from odoo import models, fields, api


class ProjectTask(models.Model):
    _inherit = 'project.task'

    for_reviewer = fields.Boolean(string='Review Task')