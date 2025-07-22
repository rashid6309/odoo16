from odoo import models, fields, api
from datetime import datetime

class ProjectProject(models.Model):
    _inherit = 'project.project'

    reviewer = fields.Many2one('res.users', string='Reviewer', tracking=True)
    x_studio_surveyor = fields.Many2one('res.users', string='Surveyor', tracking=True)
    x_studio_inital_reserve = fields.Float(string='Initial', tracking=True)
    x_studio_revised_reserve = fields.Monetary(string='Revised', tracking=True)
    x_studio_final = fields.Monetary(string='Final', tracking=True)
    final_outcome_id = fields.Many2one('final.outcome', string='Final Outcome', help='Final Outcome', tracking=True)
    x_studio_vehicle_owner = fields.Many2one('res.partner', string='Vehicle Owner', tracking=True)
    x_vehicle_owner_mobile = fields.Char(related='x_studio_vehicle_owner.mobile', string='Vehicle Owner Mobile', tracking=True)
    requestor_id = fields.Many2one(
        'res.partner', 
        string='Requestor', 
        tracking=True, 
        domain="[('parent_id', '=', partner_id)]"
    )
    timer_start = fields.Datetime(string='Timer Start', readonly=True)
    timer_duration = fields.Float(string='Active SLA Hrs', compute='_compute_timer_duration', store=True)
    timer_total_duration = fields.Float(string='Total Timer Duration', default=0.00)
    timer_pause = fields.Boolean(string='Timer Pause', default=False)

    @api.depends('timer_start')
    def _compute_timer_duration(self):
        for project in self:
            if not project.timer_pause and project.timer_start:
                now = datetime.now()
                start_time = fields.Datetime.from_string(project.timer_start)
                delta = (now - start_time).total_seconds() / 3600.0
                project.timer_duration = delta + project.timer_total_duration
            else:
                project.timer_duration = project.timer_total_duration

    def compute_timer_duration(self):
        for project in self:
            if not project.timer_pause and project.timer_start:
                now = datetime.now()
                start_time = fields.Datetime.from_string(project.timer_start)
                delta = (now - start_time).total_seconds() / 3600.0
                project.timer_duration = delta + project.timer_total_duration
            else:
                project.timer_duration = project.timer_total_duration

    @api.model
    def create(self, vals):
        project = super(ProjectProject, self).create(vals)
        if project.stage_id.name == 'New':
            project.timer_pause = False
            project.timer_start = datetime.now()
        return project

    def write(self, vals):
        for project in self:        

            if 'stage_id' in vals and vals['stage_id'] != project.stage_id.id:
                new_stage_id = vals['stage_id']
                new_stage = self.env['project.project.stage'].browse(new_stage_id).name

                if new_stage in ['Pending Info','On Hold by Client','Completed','Cancelled','Pending Client Feedback']:
                    now = datetime.now()
                    start_time = fields.Datetime.from_string(project.timer_start)
                    elapsed = (now - start_time).total_seconds() / 3600.0
                    elapsed += project.timer_total_duration 
                    vals['timer_total_duration'] = elapsed
                    vals['timer_start'] = None 
                    vals['timer_pause'] = True
                elif new_stage in ['In Progress', 'Pending Peer Review','New','Pending Peer Review']:
                    if project.timer_pause or not project.timer_start :
                        vals['timer_start'] = datetime.now()
                        vals['timer_pause'] = False
            

        result = super(ProjectProject, self).write(vals)
        return result