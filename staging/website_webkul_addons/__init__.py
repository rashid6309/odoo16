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

from odoo import api, SUPERUSER_ID
from . import models
from . import wizard

def pre_init_check(cr):
    from odoo.service import common
    from odoo.exceptions import ValidationError
    version_info = common.exp_version()
    server_serie =version_info.get('server_serie')
    if server_serie!='16.0':raise ValidationError('Module support Odoo series 16.0 found {}.'.format(server_serie))
