odoo.define('payment_moyasar_bizople.payment_form_mixin_moyasar', require => {
    'use strict';

    const checkoutForm = require('payment.checkout_form');
    const manageForm = require('payment.manage_form');

    const MoyasarPaymentCheckout = {
    	_processRedirectPayment: function (code, providerId, processingValues) {
            if (code !== 'moyasar'){
                return this._super(...arguments);
            }
            $('#moyasarpayment').modal('show');
            $('#wrapwrap').css('z-index',1051)
            return
        },
    }

    checkoutForm.include(MoyasarPaymentCheckout);
    manageForm.include(MoyasarPaymentCheckout);
})