# -*- coding: utf-8 -*-
import logging

import odoo
from odoo import http
from odoo.http import request
from odoo.tools.translate import _
from odoo.addons.web.controllers.utils import ensure_db
from odoo.addons.web.controllers.home import SIGN_UP_REQUEST_PARAMS
from odoo.addons.web.controllers.home import Home
from odoo.addons.access_restriction_by_ip.exceptions import IpAllowedDenied
_logger = logging.getLogger(__name__)



class HomeExtend(Home):

    @staticmethod
    def check_allowed_ip(ip_address):
        user_rec = request.env['res.users'].sudo().search([('login', '=', request.params['login']),
                                                           ('active', '=', True)])

        if user_rec.has_group('access_restriction_by_ip.group_ec_medical_allowed_ip'):
            return True

        ip_rec = request.env['allowed.ips'].search(domain=[('ip_address', '=', ip_address)])
        if not ip_rec:
            return False

        return True

    @http.route('/web/login', type='http', auth="none")
    def web_login(self, redirect=None, **kw):
        """
        Overrided default implementation.
        :param redirect:
        :param kw:
        :return:
        """
        remote_ip_address = request.httprequest.remote_addr

        ensure_db()
        request.params['login_success'] = False
        if request.httprequest.method == 'GET' and redirect and request.session.uid:
            return request.redirect(redirect)

        # simulate hybrid auth=user/auth=public, despite using auth=none to be able
        # to redirect users when no db is selected - cfr ensure_db()
        if request.env.uid is None:
            if request.session.uid is None:
                # no user -> auth=public with specific website public user
                request.env["ir.http"]._auth_method_public()
            else:
                # auth=user
                request.update_env(user=request.session.uid)

        values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            try:
                is_allowed = HomeExtend.check_allowed_ip(ip_address=remote_ip_address)
                if not is_allowed:
                    raise IpAllowedDenied()

                uid = request.session.authenticate(request.db, request.params['login'], request.params['password'])
                request.params['login_success'] = True
                return request.redirect(self._login_redirect(uid, redirect=redirect))
            except odoo.exceptions.AccessDenied as e:
                if e.args == odoo.exceptions.AccessDenied().args:
                    values['error'] = _("Wrong login/password")
                else:
                    values['error'] = e.args[0]
            except IpAllowedDenied as ip:
                values['error'] = ip.args[0]
        else:
            if 'error' in request.params and request.params.get('error') == 'access':
                values['error'] = _('Only employees can access this database. Please contact the administrator.')

        if 'login' not in values and request.session.get('auth_login'):
            values['login'] = request.session.get('auth_login')

        if not odoo.tools.config['list_db']:
            values['disable_database_manager'] = True

        response = request.render('web.login', values)
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['Content-Security-Policy'] = "frame-ancestors 'self'"
        return response
