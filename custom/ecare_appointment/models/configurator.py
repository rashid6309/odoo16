from odoo import models, api, fields

from odoo.exceptions import AccessError


class SlotConfigurator(models.Model):
    _name = "ec.slot.configurator"
    _description = "Configurator for the slots"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    _order = "create_date desc"

    category = fields.Many2one(comodel_name='ec.slot.category',
                               domain=[('parent_category_id', '!=', False)],
                               copy=False,
                               string="Secondary Category")

    parent_category_id = fields.Many2one(related="category.parent_category_id",
                                         string="Primary Category")

    sub_category = fields.Many2many(comodel_name='ec.slot.sub.category',
                                    string="Tertiary Categories",
                                    relation="ec_slot_configurator_ec_slot_sub_category_rel",
                                    column1="ec_slot_configurator_id",
                                    column2="ec_slot_sub_category_id",
                                    )

    slot_schedule = fields.One2many(comodel_name="ec.slot.schedule",
                                    inverse_name="configurator",
                                    string="Schedule",
                                    copy=True,
                                    )

    state = fields.Selection(selection=[('draft', 'Draft'),
                              ('active', 'Active'),
                              ('inactive', 'Inactive'),
                              ], default='draft',
                             copy=False,
                             tracking=True,
                             string='State')

    start_date = fields.Date(string='Start From',
                             tracking=True,
                             copy=False)

    end_date = fields.Date(string='End Date',
                           tracking=True,
                           default=None)

    schedule = fields.Boolean(default=False,
                              compute='_compute_schedule_slots')

    timespan = fields.Integer(string="Duration (minutes)",
                              default=60)

    @api.onchange('timespan')
    def _onchange_timespan(self):
        if self.timespan <= 0:
            return {

                'warning': {

                    'title': 'Warning!',

                    'message': 'Timespan should be greater than 0.'}

            }

    # @api.onchange('category')
    # def _onchange_category_fetch_sub_categories(self):
    #     fetch_category = self.env['ec.slot.category'].search([('id', '=', self.category.id)])
    #     if fetch_category:
    #         sub_categories = self.env['ec.slot.sub.category'].search([('id', 'in', fetch_category.sub_categories.ids)])
    #         self.sub_category = sub_categories
    # # days_availability

    def name_get(self):
        return [(self.id, 'Slot Configurator')]

    @api.onchange('start_date')
    def check_start_date(self):
        fetch_config_with_greater_date = self.env['ec.slot.configurator'].search(
            [
                ('category', '=', self.category.id),
                ('end_date', '>=', self.start_date),
            ]
        )
        if fetch_config_with_greater_date:
            self.start_date = None
            raise AccessError("Configurator's Start Date should be "
                              "greater than previous' most recent End Date.")
        if self.end_date:
            if self.start_date > self.end_date:
                self.start_date = None
                raise AccessError('Start date should be less than end date.')

    @api.onchange('end_date')
    def check_end_date(self):
        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                self.end_date = None
                raise AccessError('Start date should be less than end date.')

    @api.onchange('category')
    def check_category(self):
        if self.category:
            fetch_configuration = self.env['ec.slot.configurator'].search(
                [
                    ('category', '=', self.category.id),
                    ('state', '=', 'active'),
                ]
            )
            if fetch_configuration:
                self.state = 'draft'
                raise AccessError('Another configuration for this category is already active.')

    def action_active_configuration(self):
        if self.start_date:
            if not self.slot_schedule:
                raise AccessError("Schedule can't be empty.")
            fetch_configuration = self.env['ec.slot.configurator'].search(
                [
                    ('category', '=', self.category.id),
                    ('state', '=', 'active'),
                ]
            )
            if fetch_configuration:
                self.state = 'draft'
                raise AccessError('Another configuration for this category is already active.')
            else:
                self.state = 'active'
        else:
            raise AccessError("Start Date Can't be empty.")

    def action_in_active_configuration(self):
        if self.end_date is False:
            raise AccessError("End Date Can't be empty, End Date should be greater than start date. ")
        record = self.env['ec.booked.slot.record'].search([
            ('date', '>=', self.end_date),
            ('category', '=', self.category.id),
            ('state', '=', 'Booked'),
        ])
        if record:
            for rec in record:
                rec.state = 'Rescheduled Required'
                rec.configurator = self.id
        self.state = 'inactive'
        # self.end_date = datetime.date.today()

    @api.model
    def _compute_schedule_slots(self):
        for line in self:
            appointments = self.env['ec.booked.slot.record'].search([
                ('configurator', '=', line.id),
                ('state', '=', 'Rescheduled Required'),
            ])
            if appointments:
                line.schedule = True
            else:
                line.schedule = False

    def action_open_configurator_slots(self):
        appointments = self.env['ec.booked.slot.record'].search([
            ('configurator', '=', self.id),
            ('state', '=', 'Rescheduled Required'),
        ])
        if appointments:
            action = self.env["ir.actions.actions"]._for_xml_id("ecare_appointment.booked_slots_record_action")
            action["domain"] = [
                    ('configurator', '=', self.id),
                    ('state', '=', 'Rescheduled Required'),

                ]
            return action
        else:
            raise AccessError("No Appointments exist.")

    def action_edit_sub_categories_configuration(self):
        configurator = self.id
        default_categories = None

        if configurator:
            if self.sub_category:
                default_categories = self.sub_category.ids
            return {
                'name': 'Edit Sub-Categories',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'ec.slot.sub.category.configurator',
                'target': 'new',
                'context': {
                    'default_configurator': configurator,
                    'default_sub_category': default_categories
                }
            }
