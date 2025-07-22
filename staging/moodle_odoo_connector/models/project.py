from datetime import datetime

from odoo import models, fields, api, _
import requests

from odoo.exceptions import AccessError, UserError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    # reviewer = fields. Many2one('res.users', string='Reviewer', tracking=True)
    # x_studio_surveyor = fields.Many2one('res.users', string='Surveyor', tracking=True)
    # x_studio_inital_reserve = fields. Float(string='Initial', tracking=True) x_studio_revised_reserve = fields. Monetary(string='Revised', tracking=True)
    # x_studio_final = fields.Monetary(string='Final', tracking=True)
    # final_outcome_id = fields.Many2one('final.outcome', string='Final Outcome', help='Final Outcome', tracking=True)
    # x_studio_vehicle_owner = fields.Many2one('res.partner', string='Vehicle Owner', tracking=True)
    # x_vehicle_owner_mobile= fields.Char(related='x_studio_vehicle_owner.mobile', string='Vehicle Owner Mobile', tracking=True)
    # requestor_id = fields.Many2one( 'res.partner',
    # string='Requestor', tracking=True, domain="[('parent_id', '=', partner_id)]")
    # timer_start = fields.Datetime(string='Timer Start', readonly=True)
    # timer_duration = fields. Float(string='Active SLA Hrs', compute='_compute_timer_duration', store=False)
    # timer_total_duration = fields.Float(string="Total Timer Duration', default=0.00")
    # timer_pause = fields.Boolean(string='Timer Pause', default=False)
    #
    boolean = fields.Boolean(string='Timer Pause', default=False, compute='_compute_timer_duration')

    # @api.depends('timer_start')
    # def _compute_timer_duration(self):
    #     for project in self:
    #     if not project.timer_pause and project.timer_start:
    #         pass
    #     else:
    #         now = datetime.now()
    #         start_time = fields.Datetime.from_string (project.timer_start)
    #         delta = (now - start_time).total_seconds() / 3600.0
    #         project.timer_duration - delta + project.timer_total_duration
    #         project.timer_duration-project.timer_total_duration

    def _compute_timer_duration(self):
        pass

