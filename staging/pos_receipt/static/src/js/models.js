odoo.define('pos_receipt.models', function (require) {
    "use strict";

    const utils = require("web.utils");
    var { Orderline } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const ProductInfoPopup = Registries.Component.get('ProductInfoPopup');


    const OrderLinePosReceipt = (Orderline) => class OrderLinePosReceipt extends Orderline {
        constructor(obj, options) {
            super(obj, options);
            this.internal_reference = options.internal_reference;
            this.location_name = options.location_name;
        }
        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.internal_reference = json.internal_reference;
            this.location_name = json.location_name;
        }

        get_internal_reference () {
            return this.product.default_code;
        }
        get_location_name () {
            return this.location_name;
        }
        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.internal_reference = this.get_internal_reference();
            json.location_name = this.get_location_name();
            return json;
        }

        export_for_printing() {
            var line = super.export_for_printing(...arguments);
            line.internal_reference = this.get_product().default_code;
            line.location_name = this.get_location_name();
            return line;
        }
    }
    Registries.Model.extend(Orderline, OrderLinePosReceipt);

    utils.patch(ProductInfoPopup.prototype, 'ProductInfoPopupPosReceipt', {
        autoSelectDefaultLocationPosReceipt() {
            let default_location_id = this.env.pos.config.location_id[0];
            // window.localStorage.setItem(
            //     'selected_order_line_location_id', this.env.pos.selectedOrder.selected_orderline.location_id || false
            // );
            setTimeout(function(argument) {
                let locations = $('.location_id');
                for (var i = locations.length - 1; i >= 0; i--) {
                    if (parseInt(locations[i].value) === default_location_id) {
                        locations[i].click();
                    }
                    // else if (parseInt(window.localStorage.selected_order_line_location_id)
                    //     === parseInt(locations[i].dataset.id)) {
                    //     locations[i].click()
                    // }
                }
            }, 50);
        },

        onChangeOrderLinePickingLocationIDAndName(event) {
            let location_id = parseInt($(event.target).val());
            this.env.pos.selectedOrder.selected_orderline.location_id = location_id;
            this.env.pos.selectedOrder.selected_orderline.location_name = event.target.dataset.name;
        }
    });
});
