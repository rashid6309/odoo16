from odoo import http
from odoo.http import request

class ScreenLockController(http.Controller):

   @http.route('/screen_lock/check', type='json', auth='user')
   def check_lock_status(self):
       user = request.env.user
       return {'locked': bool(user.screen_lock_pin)}

   @http.route('/screen_lock/verify', type='json', auth='user')
   def verify_pin(self, pin):
       user = request.env.user
       if user.screen_lock_pin and user.screen_lock_pin == pin:
           return {'success': True}
       return {'success': False}