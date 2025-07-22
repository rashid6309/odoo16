odoo.define('pos_orders_adv_search.TicketScreen', function (require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');

    const CustomTicketScreen = (TicketScreen) =>
        class extends TicketScreen {
            _getSearchFields() {
                const fields = super._getSearchFields(...arguments);
                fields.INVOICE_NUMBER = {
                    repr: (order) => order.get_account_move_name(),
                    displayName: this.env._t('Invoice Number'),
                    modelField: 'account_move.name',
                }
                fields.ORDER_REF = {
                    repr: (order) => order.get_account_move_origin(),
                    displayName: this.env._t('Order Ref'),
                    modelField: 'name',
                }
                return fields;
            }

            getInvoice(order) {
                return order.get_account_move_name();
            }

            getInvoiceOrigin(order) {
                return order.get_account_move_origin();
            }
        };

    Registries.Component.extend(TicketScreen, CustomTicketScreen);

    return TicketScreen;
});
