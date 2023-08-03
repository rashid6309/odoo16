# -*- coding: utf-8 -*-
from odoo import models, fields, api



class AllowedIPs(models.Model):
    _name = 'allowed.ips'

    ip_address = fields.Char(string='Allowed IP',
                             required=True)

    description = fields.Char(string='Description')

    active = fields.Boolean(string='Active',
                            default=True)

    _sql_constraints = [('ip_address_uniq', 'unique(ip_address)', 'The IP address must be unique')]

    def name_get(self):
        return [(self.id, 'Allowed IPs')]