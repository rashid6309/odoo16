odoo.define('pos_orders_adv_search.pos', function (require) {
    "use strict";

    var { PosGlobalState, Order } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');

    const PosAdvSearchGlobalState = (PosGlobalState) => class PosAdvSearchGlobalState extends PosGlobalState {
        async _processData(loadedData) {
            await super._processData(...arguments);
            // this.account_move = loadedData['account.move'];
            this.account_move_by_id = loadedData['account_move_by_id'];
        }
    }
    Registries.Model.extend(PosGlobalState, PosAdvSearchGlobalState);


    const PosAdvSearchOrder = (Order) => class PosAdvSearchOrder extends Order {
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            if (json.account_move) {
                this.invoice = this.pos.account_move_by_id[json.account_move];
            }
        }
        get_account_move_name() {
            let account_move = this.invoice;
            return account_move ? account_move.name : "";
        }
        get_account_move_origin() {
            let account_move = this.invoice;
            return account_move ? account_move.ref : "";
        }
        wait_for_push_order() {
            var result = super.wait_for_push_order(...arguments);
            result = Boolean(result || this.pos.config.allow_invoice_number_search || this.pos.config.allow_order_ref_search);
            return result;
        }
    }
    Registries.Model.extend(Order, PosAdvSearchOrder);

});