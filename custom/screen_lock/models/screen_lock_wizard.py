from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ScreenLockWizard(models.TransientModel):
    _name = 'screen.lock.wizard'
    _description = 'Screen Lock PIN Configuration'

    pin = fields.Char(string='PIN', size=4, required=True)
    confirm_pin = fields.Char(string='Confirm PIN', size=4, required=True)

    @api.constrains('pin')
    def _check_pin_format(self):
        for record in self:
            if record.pin and (not record.pin.isdigit() or len(record.pin) != 4):
                raise UserError(_('PIN must be exactly 4 digits.'))

    def set_pin(self):
        self.ensure_one()
        if self.pin != self.confirm_pin:
            raise UserError(_('PIN and Confirm PIN do not match.'))
        
        # Set PIN directly on the current user
        self.env.user.write({'screen_lock_pin': self.pin})
        
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Screen Lock PIN has been set successfully.'),
                'type': 'success',
                'sticky': False,
            }
        }