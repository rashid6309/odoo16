from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    project_id = fields.Many2one('project.project')
    project_status = fields.Char(string="Project Status", related='project_id.stage_id.name')