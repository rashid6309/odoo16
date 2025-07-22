from odoo import models, fields, api

class ScreenLockWizard(models.TransientModel):
    _name = 'screen.lock.wizard'
    _description = 'Screen Lock Wizard'

    pin = fields.Char(string='PIN', size=4, required=True)

    def set_pin(self):
        user = self.env.user
        lock = self.env['screen.lock'].search([('user_id', '=', user.id)], limit=1)
        if lock:
            lock.write({'pin': self.pin})
        else:
            self.env['screen.lock'].create({'user_id': user.id, 'pin': self.pin})
        return {'type': 'ir.actions.act_window_close'}