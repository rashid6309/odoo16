# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import _, api, fields, models

class PaymentAcquirerMoyasar(models.Model):
    _inherit = 'payment.provider'

    def _valid_field_parameter(self, field, name):
        return name == 'domain'or super()._valid_field_parameter(field, name)

    code = fields.Selection(
        selection_add=[('moyasar', 'Moyasar')], ondelete={'moyasar': 'set default'}
    )
    moyasar_public_key = fields.Char(string='Public Key', required_if_provider='moyasar', domain="[('code', '=', 'moyasar')]")
    moyasar_secret_key = fields.Char(string='Secret Key', required_if_provider='moyasar', domain="[('code', '=', 'moyasar')]")
    apple_pay_file = fields.Binary("Applepay Merchant file", domain="[('code', '=', 'moyasar')]")

    @api.constrains('apple_pay_file')
    def create_ir_attach_applepay(self):
        attachment_id = self.env['ir.attachment'].sudo().create({
            'name': 'apple-developer-merchantid-domain-association',
            'type': 'binary',
            'res_model': 'payment.provider',
            'datas': self.apple_pay_file,
            'access_token' : self.env['ir.attachment']._generate_access_token()
        })
        return attachment_id