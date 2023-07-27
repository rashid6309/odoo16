# -*- coding: utf-8 -*-
##############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2017-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Niyas Raphy(<https://www.cybrosys.com>)
#    you can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC LICENSE
#    GENERAL PUBLIC LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from odoo import models, fields, api


#
# class ResUsersInherit(models.Model):
#     _inherit = 'res.users'
#
#     allowed_ips = fields.One2many('allowed.ips', 'users_ip', string='IP')


class AllowedIPs(models.Model):
    _name = 'allowed.ips'

    # users_ip = fields.Many2one('res.users', string='IP User')
    ip_address = fields.Char(string='Allowed IP')
    description = fields.Char(string='Description')
    is_active = fields.Boolean(string='Is Active')
    _sql_constraints = [('ip_address_uniq', 'unique(ip_address)', 'The IP address must be unique')]

    def name_get(self):
        return [(self.id, 'Allowed IPs')]