from odoo import models, api, fields


from odoo.addons.ecare_core.utilities.helper import TimeValidation, CustomNotification


class SlotSchedule(models.Model):
    _name = "ec.slot.schedule"
    _description = "Schedule of Slot"

    configurator = fields.Many2one('ec.slot.configurator')

    day = fields.Selection([('0', 'Monday'), ('1', 'Tuesday'),
                            ('2', 'Wednesday'), ('3', 'Thursday'),
                            ('4', 'Friday'),
                            ('5', 'Saturday'),
                            ('6', 'Sunday'),
                            ], default="0", string='Day')

    active_time = fields.Char('From', required=True, tracking=True)
    to_time = fields.Char('To', required=True, tracking=True)


    @api.onchange('active_time', 'to_time')
    def _onchange_time(self):
        if self.to_time:
            time = TimeValidation.validate_time(self.to_time)

            if not time:
                return CustomNotification.notification_time_validation()

            self.to_time = time

        if self.active_time:
            time = TimeValidation.validate_time(self.active_time)

            self.active_time = time
            if not time:
                return CustomNotification.notification_time_validation()
