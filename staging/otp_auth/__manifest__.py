# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
{
  "name"                 :  "Website OTP Authentication",
  "summary"              :  """Odoo Website OTP Authentication makes secure environment in your odoo website for your portal users.""",
  "category"             :  "Website",
  "version"              :  "2.1.0",
  "sequence"             :  1,
  "author"               :  "Webkul Software Pvt. Ltd.",
  "license"              :  "Other proprietary",
  "website"              :  "https://store.webkul.com/Odoo-Website-OTP-Authentication.html",
  "description"          :  """OTP
One Time Authentication Password
OTP Authentication
Website OTP Authentication
Odoo Website OTP Authentication
One Time Password
One Time Password Authentication
Access Management
SMS OTP
SMS One Time Password
Odoo OTP SMS Notification
Login via OTP
Login via OTP Authentication
Odoo
Website""",
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=otp_auth&custom_url=/web/login",
  "depends"              :  ['website_webkul_addons'],
  "data"                 :  [
                             'security/ir.model.access.csv',
                             'views/auth_signup_login_templates.xml',
                             'edi/otp_edi_template.xml',
                             'views/res_config_views.xml',
                             'views/webkul_addons_config_inherit_view.xml',
                             'data/data_otp.xml',
                            ],
  "assets"               : {
                            'web.assets_frontend': [
				    '/otp_auth/static/src/js/wk_otp.js',
				    '/otp_auth/static/src/js/wk_otp_login.js',
				    '/otp_auth/static/src/scss/wk_otp_login.scss',
        			],
                            # 'web.assets_qweb':  ['otp_auth/static/src/xml/thread.xml']
                            },
  "images"               :  ['static/description/Banner.png'],
  "application"          :  True,
  "installable"          :  True,
  "auto_install"         :  False,
  "price"                :  35,
  "currency"             :  "USD",
  "pre_init_hook"        :  "pre_init_check",
   "external_dependencies":  {'python': ['pyotp']}
}
