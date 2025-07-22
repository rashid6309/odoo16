from odoo import models, fields, api

class ScreenLock(models.Model):
   _name = 'screen.lock'
   _description = 'Screen Lock Configuration'

   user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
   pin = fields.Char(string='PIN', size=4, related='user_id.screen_lock_pin', store=True)

   @api.model
   def get_user_pin(self):
       user = self.env.user
       return user.screen_lock_pin