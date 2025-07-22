odoo.define('pos_modification.models', function(require) {
    "use strict";

    const utils = require("web.utils");
    const {
        PosGlobalState,
        Orderline
    } = require('point_of_sale.models');
    const Registries = require('point_of_sale.Registries');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const ProductInfoPopup = Registries.Component.get('ProductInfoPopup');

    const POSProductScreen = (ProductScreen) => class POSProductScreen extends ProductScreen {
        async _clickProduct(event) {
            let product = event.detail;
            if (product.free_qty < 1) {
                this.showPopup('ErrorPopup', {
                    title: this.env._t(`${product.display_name} ${product.default_code} with selling price ${product.lst_price} is out of stock `),
                    body: this.env._t('You are not allowed to add product that is out of stock to cart'),
                });
                return;
            }
            return await super._clickProduct(event);

        }
    }

    Registries.Component.extend(ProductScreen, POSProductScreen);


    const PosStockLocationPosGlobalState = (PosGlobalState) => class PosStockLocationPosGlobalState extends PosGlobalState {
        constructor(obj) {
            super(obj);
            this.locations = [];
        }
        //@override
        async _processData(loadedData) {
            await super._processData(...arguments);
            this.locations = loadedData['stock.location'];
        }

    }
    Registries.Model.extend(PosGlobalState, PosStockLocationPosGlobalState);


    utils.patch(ProductInfoPopup.prototype, "patchedProductInfoPopup", {
        autoSelectDefaultLocation() {
            let default_location_id = this.env.pos.config.location_id[0];
            setTimeout(function(argument) {
                let locations = $('.location_id');
                for (var i = locations.length - 1; i >= 0; i--) {
                    if (parseInt(locations[i].value) === default_location_id) {
                        locations[i].click();

                    }
                }
            }, 50);

        },


        onChangeOrderLinePickingLocationID(event) {
            let location_id = parseInt($(event.target).val());
            this.env.pos.selectedOrder.selected_orderline.location_id = location_id;
        }

    });

    const LocationOrderline = (Orderline) => class LocationOrderline extends Orderline {
        constructor(obj, options) {
            super(obj, options);
            this.location_id = false;

        }
        export_as_JSON() {

            let result = super.export_as_JSON(...arguments);
            result.location_id = this.location_id;
            return result;
        }


    }
    Registries.Model.extend(Orderline, LocationOrderline);


});