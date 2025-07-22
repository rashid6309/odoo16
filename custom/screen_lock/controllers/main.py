from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)


class ScreenLockController(http.Controller):

    @http.route('/screen_lock/check', type='json', auth='user')
    def check_lock_status(self):
        """Check if the current user has a PIN set up and if screen is locked"""
        try:
            user = request.env.user
            has_pin = bool(user.screen_lock_pin and len(user.screen_lock_pin) == 4)
            
            # Check session lock status
            session_locked = request.session.get('screen_locked', False)
            
            return {
                'locked': has_pin,
                'session_locked': session_locked,
                'has_pin': has_pin
            }
        except Exception as e:
            _logger.error("Error checking lock status: %s", str(e))
            return {
                'locked': False,
                'session_locked': False,
                'has_pin': False
            }

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
                # Unlock the session
                request.session['screen_locked'] = False
                _logger.info("Successful screen unlock for user: %s", user.login)
                return {'success': True}
            else:
                _logger.warning("Failed screen unlock attempt for user: %s", user.login)
                return {'success': False, 'error': 'Incorrect PIN'}
                
        except Exception as e:
            _logger.error("Error verifying PIN: %s", str(e))
            return {'success': False, 'error': 'Verification error'}

    @http.route('/screen_lock/lock_session', type='json', auth='user')
    def lock_session(self):
        """Lock the current session"""
        try:
            user = request.env.user
            
            # Check if user has a PIN configured
            if not user.screen_lock_pin:
                return {'success': False, 'error': 'No PIN configured'}
            
            # Lock the session
            request.session['screen_locked'] = True
            _logger.info("Screen locked for user: %s", user.login)
            return {'success': True}
            
        except Exception as e:
            _logger.error("Error locking session: %s", str(e))
            return {'success': False, 'error': 'Lock error'}

    @http.route('/screen_lock/unlock_session', type='json', auth='user')
    def unlock_session(self):
        """Unlock the current session (for emergency use)"""
        try:
            request.session['screen_locked'] = False
            return {'success': True}
        except Exception as e:
            _logger.error("Error unlocking session: %s", str(e))
            return {'success': False, 'error': 'Unlock error'}