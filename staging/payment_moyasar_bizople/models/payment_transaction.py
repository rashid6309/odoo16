# -*- coding: utf-8 -*-
# Developed by Bizople Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details

from odoo import _, api, models, fields
from odoo.exceptions import ValidationError

class PaymentTransactionMoyasar(models.Model):
    _inherit = 'payment.transaction'

    moyasar_payment_id = fields.Char("Moyasar Payment Id")

    @api.model
    def _get_tx_from_notification_data(self, provider_code, notification_data):
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != 'moyasar':
            return tx

        reference = notification_data.get('reference')
        tx = self.search([('reference', '=', reference), ('provider_code', '=', 'moyasar')])
        if not tx:
            raise ValidationError(
                "Moyasar: " + _("No transaction found matching reference %s.", reference)
            )
        return tx

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'moyasar':
            return

        trans_state = notification_data.get("state", False)
        if trans_state:
            self.write({
                'state_message': _("Moyasar Payment Gateway Response :-") + notification_data["state"]
            })
            if trans_state == 'done':
                self._set_done()
            elif trans_state == "pending":
                self._set_pending()
            elif trans_state == "cancel":
                self._set_canceled()