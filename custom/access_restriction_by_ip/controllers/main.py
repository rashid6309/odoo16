# -*- coding: utf-8 -*-

from odoo.addons.web.controllers import utils
from odoo.addons.web.controllers import home
from odoo.http import request
from odoo.exceptions import Warning
import odoo
import odoo.modules.registry
from odoo.tools.translate import _
from odoo import http


class Home(home.Home):

    def check_allowed_ip(self, ip_address):
        user_rec = request.env['res.users'].sudo().search([('login', '=', request.params['login'])])
        if user_rec.has_group('access_restriction_by_ip.group_ec_medical_allowed_ip'):
            return True

        ip_rec = request.env['allowed.ips'].sudo().search(domain=[('ip_address', '=', ip_address)])
        if not ip_rec:
            return False

        return True

    @http.route('/web/login', type='http', auth="public")
    def web_login(self, redirect=None, **kw):
        utils.ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)
        if not request.uid:
            request.uid = odoo.SUPERUSER_ID
        values = request.params.copy()
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None
        if request.httprequest.method == 'POST':
            old_uid = request.uid
            ip_address = request.httprequest.environ['REMOTE_ADDR']
            if request.params['login']:
                is_allowed = self.check_allowed_ip(ip_address)
                if not is_allowed:
                    values['error'] = _("Not allowed to login from this IP")
                else:
                    try:
                        uid = request.session.authenticate(request.session.db,
                                                           request.params[
                                                               'login'],
                                                           request.params[
                                                               'password'])
                        if uid:
                            request.params['login_success'] = True
                            return request.redirect(
                                self._login_redirect(uid, redirect=redirect))
                    except:
                        values['error'] = _("Wrong login/password")
                        return request.render('web.login', values)
        return request.render('web.login', values)
