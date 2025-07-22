odoo.define('pos_modification.FixedFixedDiscountButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const {
        useListener
    } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');

    class FixedDiscountButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
        async onClick() {
            var self = this;
            const {
                confirmed,
                payload
            } = await this.showPopup('NumberPopup', {
                title: this.env._t('Fixed Discount'),
                startingValue: this.env.pos.config.discount_fx,
                isInputSelected: true
            });
            if (confirmed) {
                await self.apply_discount(payload);
            }
        }

        async apply_discount(disc) {
            let order = this.env.pos.get_order();
            let lines = order.get_orderlines();
            let product = this.env.pos.db.get_product_by_id(this.env.pos.config.discount_product_id[0]);
            if (product === undefined) {
                await this.showPopup('ErrorPopup', {
                    title: this.env._t("No discount product found"),
                    body: this.env._t("The discount product seems misconfigured. Make sure it is flagged as 'Can be Sold' and 'Available in Point of Sale'."),
                });
                return;
            }
            lines.filter(line => line.get_product() === product)
                .forEach(line => order.remove_orderline(line));

            // Add one discount line per tax group
            let linesByTax = order.get_orderlines_grouped_by_tax_ids();
            for (let [tax_ids, lines] of Object.entries(linesByTax)) {

                // Note that tax_ids_array is an Array of tax_ids that apply to these lines
                // That is, the use case of products with more than one tax is supported.
                let tax_ids_array = tax_ids.split(',').filter(id => id !== '').map(id => Number(id));

                let baseToDiscount = order.calculate_base_amount(tax_ids_array, lines);

                // We add the price as manually set to avoid recomputation when changing customer.
                let discount = -disc;
                if (discount < 0) {
                    order.add_product(product, {
                        price: discount,
                        lst_price: discount,
                        tax_ids: tax_ids_array,
                        merge: false,
                        description: `${discount}, ` +
                            (tax_ids_array.length ?
                                _.str.sprintf(
                                    this.env._t('Tax: %s'),
                                    tax_ids_array.map(taxId => this.env.pos.taxes_by_id[taxId].amount + '%').join(', ')
                                ) :
                                this.env._t('No tax')),
                        extras: {
                            price_manually_set: true,
                        },
                    });
                }
            }
        }
    }
    FixedDiscountButton.template = 'FixedDiscountButton';

    ProductScreen.addControlButton({
        component: FixedDiscountButton,
        condition: function() {
            return this.env.pos.config.module_pos_discount && this.env.pos.config.discount_product_id;
        },
    });

    Registries.Component.add(FixedDiscountButton);

    return FixedDiscountButton;
});