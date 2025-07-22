# -*- coding: utf-8 -*-
#################################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   If not, see <https://store.webkul.com/license.html/>
#
#################################################################################

from odoo import http, tools,api, _
from odoo.http import request
from odoo.addons.otp_auth.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.home import ensure_db, Home, SIGN_UP_REQUEST_PARAMS
from odoo import http
from odoo.exceptions import UserError
import datetime as dt
import logging
_logger = logging.getLogger("******** OTP ********")
SIGN_UP_REQUEST_PARAMS.add('mobile')

class AuthSignupHome(AuthSignupHome):
    
    @http.route(website=True, auth="public", sitemap=False)
    def web_login(self, redirect=None, *args, **kw):
        mobile = kw.get('mobile')
        login = kw.get('login')
        if mobile:
            userObj = request.env["res.users"].sudo().search([("mobile", "=", mobile)])
            if userObj:
                loginId = userObj.login
                if loginId:
                    request.params['login'] = loginId
        response = super(AuthSignupHome, self).web_login(redirect=redirect, *args, **kw)
        if 'login_success' in request.params and request.params.get('login_success') == False:
            request.params['login'] = login
            response.qcontext['login'] = login
        return response


    def _prepare_signup_values(self, qcontext):
        values = { key: qcontext.get(key) for key in ('login', 'name', 'password','mobile') }
        values['country_id'] = int(qcontext.get('country_id',0))
        if not values:
            raise UserError(_("The form was not properly filled in."))
        if values.get('password') != qcontext.get('confirm_password'):
            raise UserError(_("Passwords do not match; please retype them."))
        supported_lang_codes = [code for code, _ in request.env['res.lang'].get_installed()]
        lang = request.context.get('lang', '')
        if lang in supported_lang_codes:
            values['lang'] = lang
        return values

    @http.route(['/send/otp'], type='json', auth="public", methods=['POST'], website=True)
    def send_otp(self, **kwargs):
        otpdata = self.getOTPData()
        otp = otpdata[0]
        otp_time = otpdata[1]
        start = dt.datetime.now()
        kwargs['otpdata'] = otpdata
        res=None
        otp_notification_mode = request.env['ir.default'].sudo().get('website.otp.settings', 'otp_notification_mode')
        if otp_notification_mode != 'sms':
            res = super(AuthSignupHome, self).send_otp(**kwargs)
        res = res if res else {}
        if otp_notification_mode != 'email':
            mobile = kwargs.get('mobile')
            if mobile:
                userObj = request.env["res.users"].sudo().search([("mobile", "=", mobile)])
                if userObj:
                    loginId = userObj.login
                    countryObj = userObj.sudo().partner_id.country_id
                    phone_code = countryObj.phone_code
                    response = request.env['send.otp'].sms_send_otp(mobile, False, otp, phone_code)
                    errorSMS = response._context.get('sms_error') if response and response._context else False
                    end = dt.datetime.now()
                    rest = (end-start).total_seconds()
                    if rest < otp_time:
                        otp_time = int(otp_time - rest)
                    if errorSMS:
                        msg = "فشل في ارسال رمز التحقق !! من فضلك تأكد من إدخال رقم الجوال الصحيح.<br/><center>or</center> <br/><p class='alert alert-danger'> Reason: {}</p>".format(errorSMS)
                        res['email'] = {'status':0, 'message':_(msg), 'otp_time':0, 'email':loginId}
                    else:
                        res['email'] = {'status':1, 'message':_("تم إرسال رمز التحقق إلى رقم الجوال. : {}.".format(mobile)), 'otp_time':otp_time, 'email':loginId}
                else:
                    res['email'] = {'status':0, 'message':_("فشل في ارسال رمز التحقق !! من فضلك تأكد من إدخال رقم الجوال الصحيح."), 'otp_time':0, 'email':False}
        elif not kwargs.get('email') and res.get('email', {}).get('status') == 0:
            res['email'] = {'status':0, 'message':_("فشل في ارسال رمز التحقق !! من فضلك تأكد من إدخال بريد الإكتروني صحيح."), 'otp_time':0, 'email':False}
        return res

    
    @http.route(['/get/user/email'], type='json', auth="public", methods=['POST'], website=True)
    def get_user_email(self, **kwargs):
        mobile = kwargs.get('mobile')
        login = kwargs.get('login')
        resp = {}
        if not mobile and login:
            userObj = request.env["res.users"].sudo().search([("login", "=", login)], limit=1)
            mobile = userObj.mobile if userObj else False
        elif mobile and not login:
            userObj = request.env["res.users"].sudo().search([("mobile", "=", mobile)], limit=1)
            login = userObj.login if userObj else False
        
        if login and mobile:
            resp = {'status':1, 'message':_("Mobile No. : {}.".format(mobile)), 'mobile':mobile, 'login':login}
        elif not login and mobile:
            resp = {'status':0, 'message':_("فشل تسجيل الدخول !! من فضلك تأكد من إدخال رقم الجوال الصحيح."), 'mobile':mobile, 'login':False}
        elif not mobile and login:
            resp = {'status':0, 'message':_("فشل تسجيل الدخول !! من فضلك تأكد من إدخال المعرف الصحيح."), 'mobile':False, 'login':login}
        else:
            resp = {'status':0, 'message':_("فشل تسجيل الدخول !! من فضلك أدخل رقم الجوال / المعرف الصحيح"), 'mobile':False, 'login':False}
        return resp

    @http.route(['/generate/otp'], type='json', auth="public", methods=['POST'], website=True)
    def generate_otp(self, **kwargs):
        mobile = kwargs.get('mobile')
        if not mobile:
            return [0, _("Please enter a mobile no"), 0]
        res = super(AuthSignupHome, self).generate_otp(**kwargs)
        if len(res) > 0 and res[0] == 1:
            otp_notification_mode = request.env['ir.default'].sudo().get('website.otp.settings', 'otp_notification_mode')
            if otp_notification_mode != 'email':
                if mobile and res:
                    if otp_notification_mode == 'both':
                        res[1] = "{} and Mobile No: {}".format(res[1], mobile)
                    elif otp_notification_mode == 'sms':
                        res[1] = "OTP has been sent to given Mobile No: {}".format(mobile)
                        res[0] = 1
        return res

    def checkExistingUser(self, **kwargs):
        message = False
        otp_notification_mode = request.env['ir.default'].sudo().get('website.otp.settings', 'otp_notification_mode')
        if otp_notification_mode != 'sms':
            message = super(AuthSignupHome, self).checkExistingUser(**kwargs)
        mobile = kwargs.get('mobile')
        userObj = request.env["res.users"].sudo().search([("mobile", "=", mobile)])
        if userObj:
            val = "مستخدم آخر مسجل بالفعل مع {} هذا الرقم!!".format(mobile)
            message = [0, _(val), 0]
        if not message:
            message = [0, _("OTP can't send because email OTP notification is not enabled."), 0]
        return message

    def sendOTP(self, otp, **kwargs):
        res = super(AuthSignupHome, self).sendOTP(otp, **kwargs)
        userName = kwargs.get('userName')
        mobile = kwargs.get('mobile')
        country = kwargs.get('country')
        phone_code = False
        if country:
            country = int(country)
            countryObj = request.env['res.country'].sudo().browse(country)
            phone_code = countryObj.phone_code
        test = request.env['send.otp'].sms_send_otp(mobile, userName, otp, phone_code)
        return res
