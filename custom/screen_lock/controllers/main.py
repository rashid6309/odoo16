from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class ScreenLockController(http.Controller):

    @http.route('/screen_lock/check', type='json', auth='user')
    def check_lock_status(self):
        """Check if the current user has a PIN set up"""
        try:
            user = request.env.user
            has_pin = bool(user.screen_lock_pin and len(user.screen_lock_pin) == 4)
            return {'locked': has_pin}
        except Exception as e:
            _logger.error("Error checking lock status: %s", str(e))
            return {'locked': False}

    @http.route('/screen_lock/verify', type='json', auth='user')
    def verify_pin(self, pin):
        """Verify the provided PIN against the user's stored PIN"""
        try:
            user = request.env.user
            
            # Basic validation
            if not pin or len(str(pin)) != 4 or not str(pin).isdigit():
                return {'success': False, 'error': 'Invalid PIN format'}
            
            # Check if user has a PIN set
            if not user.screen_lock_pin:
                return {'success': False, 'error': 'No PIN configured'}
            
            # Verify PIN
            if user.screen_lock_pin == str(pin):
                _logger.info("Successful screen unlock for user: %s", user.login)
                return {'success': True}
            else:
                _logger.warning("Failed screen unlock attempt for user: %s", user.login)
                return {'success': False, 'error': 'Incorrect PIN'}
                
        except Exception as e:
            _logger.error("Error verifying PIN: %s", str(e))
            return {'success': False, 'error': 'Verification error'}