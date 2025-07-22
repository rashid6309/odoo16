odoo.define('pos_orders_adv_search.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');

    const PosAdvSearchPaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
            async _postPushOrderResolve(order, order_server_ids) {
                try {
                    const result = await this.rpc({
                        model: 'pos.order',
                        method: 'get_invoice',
                        args: [order_server_ids],
                    });
                    if (result) {
                        this.env.pos.account_move_by_id[result.id] = result
                    }
                } finally {
                    return super._postPushOrderResolve(...arguments);
                }
            }
        };

    Registries.Component.extend(PaymentScreen, PosAdvSearchPaymentScreen);

    return PaymentScreen;
});