odoo.define('pos_receipt.PosReceiptButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
    const { isConnectionError } = require('point_of_sale.utils');
    const { Gui } = require('point_of_sale.Gui');
    const { nextFrame } = require('point_of_sale.utils');
    const { useRef } = owl;
    const { ConnectionLostError, ConnectionAbortedError } = require('@web/core/network/rpc_service')
    const { identifyError } = require('point_of_sale.utils');

    class PosReceiptButton extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
            this.orderReceipt = useRef('order-receipt');
        }
        get currentOrder() {
            return this.env.pos.get_order();
        }
        async onClick() {
            try {
                // LegacyComponent doesn't work the same way as before.
                // We need to use Gui here to show the screen. This will work
                // because ui methods in Gui is bound to the root component.
                // const screen = 'ReceiptScreenPosReceipt';
                // Gui.showScreen(screen);
                const orderlines = this.env.pos.get_order().get_orderlines();
                for (const orderline of orderlines) {
                    if (!orderline.location_id && !orderline.location_name) {
                        const product = orderline.get_product();
                        const quantity = orderline.get_quantity();
                        try {
                            const info = await this.env.pos.getProductInfo(product, quantity);
                            orderline.location_id = info.productInfo.quants[0].id;
                            orderline.location_name = info.productInfo.quants[0].name;
                        } catch (e) {
                            if (identifyError(e) instanceof ConnectionLostError||ConnectionAbortedError) {
                                this.showPopup('OfflineErrorPopup', {
                                    title: this.env._t('Network Error'),
                                    body: this.env._t('Cannot access product information screen if offline.'),
                                });
                            } else {
                                this.showPopup('ErrorPopup', {
                                    title: this.env._t('Unknown error'),
                                    body: this.env._t('An unknown error prevents us from loading product information.'),
                                });
                            }
                        }
                    }
                }
                var printFrame = document.createElement('iframe');
                printFrame.style.display = 'none';
                document.body.appendChild(printFrame);
                var printWindow = printFrame.contentWindow;
                printWindow.document.open();
                var content = this.renderOrderReceiptPosReceipt();
                printWindow.document.write(content);
                printWindow.document.close();
                printWindow.print();
            } catch (error) {
                if (isConnectionError(error)) {
                    this.showPopup('ErrorPopup', {
                        title: this.env._t('Network Error'),
                        body: this.env._t('Cannot access order management screen if offline.'),
                    });
                } else {
                    throw error;
                }
            }
        }

        renderOrderReceiptPosReceipt() {
            var pos = this.env.pos;
            let html = `
                <div class="pos-receipt" style="text-align: center;">
                <img class="pos-receipt-logo" src="${pos.company_logo_base64}" height="30" alt="Logo"/>
              </div>
              <br/><br/>
              `;

            html += `
    <div class="pos-receipt-contact" style="text-align: center; font-size: small">
  `;

            if (pos.company.contact_address) {
                html += `
      <div>${pos.company.contact_address}</div>
    `;
            }

            if (pos.company.phone) {
                html += `
      <div>Tel:${pos.company.phone}</div>
    `;
            }

            if (pos.company.vat) {
                html += `
      <div>${pos.company.vat_label ? pos.company.vat_label + ": " : ""}${pos.company.vat}</div>
    `;
            }

            if (pos.company.email) {
                html += `
      <div>${pos.company.email}</div>
    `;
            }

            if (pos.company.website) {
                html += `
      <div>${pos.company.website}</div>
    `;
            }

            if (pos.header_html) {
                html += `
      ${pos.header_html}
    `;
            } else if (pos.header) {
                html += `
      <div style="white-space:pre-line">${pos.header}</div>
    `;
            }

            if (pos.cashier) {
                html += `
      <div class="cashier">
        <div>--------------------------------</div>
        <div>Served by ${pos.cashier.name}</div>
      </div>
    `;
            }

            html += `
    </div>
    <br /><br />
    <div class="pos-receipt-header" style="text-align: center; font-size: 24px;">
      <span id="title_english">Prepare Order Receipt</span>
    </div>
    <div class="pos-receipt-header" style="text-align: center; font-size: 24px;">
      <span id="title_arabic">تحضير إيصال الطلب</span>
    </div>
    <br /><br />
    <div class="orderlines">
    <table class="table" style="border: solid #0f0f0f 1px;">
      <thead style="display: table-row-group;">
        <tr style="border-bottom: solid #0f0f0f 1px;">
          <th style="text-align: center; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">No.</th>
          <th style="text-align: center; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">Name</th>
          <th style="text-align: center; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">Internal Reference</th>
          <th style="text-align: center; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">QTY</th>
          <th style="text-align: center; border-bottom: solid #0f0f0f 1px;">Location</th>
        </tr>
      </thead>
      <tbody>
      ${this.renderOrderLinesReceipt()}
    </div>
    <br/>
    <div t-if="receipt.footer_html"  class="pos-receipt-center-align">
        <p style="font-size: smaller; text-align: center;">${pos.orders[0].name}</p>
        <p style="font-size: smaller; text-align: center;">${pos.orders[0].creation_date.toLocaleDateString("en-US")} ${pos.orders[0].creation_date.toLocaleTimeString("en-US")}</p>
    </div>
  </div>
  `;

            return html;
        }

        renderOrderLinesReceipt() {
            var orderlines = this.env.pos.selectedOrder.orderlines;
            let html = ``;

            orderlines.forEach((line, index) => {
                html += `
      <tr>
        ${index === orderlines.length - 1 ? `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px;">
          ${index + 1}
        </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">
          ${index + 1}
        </td>
        `}
        
        ${index === orderlines.length - 1 ? `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px;">
          ${line.full_product_name ? line.full_product_name : line.product.display_name}
        </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">
          ${line.full_product_name ? line.full_product_name : line.product.display_name}
        </td>
        `}
        ${index === orderlines.length - 1 ? `
          ${line.product.default_code.length > 10 ? `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px;">
            ${line.product.default_code.substring(0, 5)}-${line.product.default_code.substring(5)}
          </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px;">
            ${line.product.default_code}
          </td>
        `}
        ` : `
          ${line.product.default_code.length > 10 ? `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">
            ${line.product.default_code.substring(0, 5)}-${line.product.default_code.substring(5)}
          </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">
            ${line.product.default_code}
          </td>
        `}
        `}
        ${index === orderlines.length -1 ? `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px;">
          ${line.quantity}
        </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-right: solid #0f0f0f 1px; border-bottom: solid #0f0f0f 1px;">
          ${line.quantity}
        </td>
        `}
        
        ${index === orderlines.length -1 ? `
          <td style="text-align: center; font-size: smaller;">
          ${line.location_name || ""}
        </td>
        ` : `
          <td style="text-align: center; font-size: smaller; border-bottom: solid #0f0f0f 1px;">
          ${line.location_name || ""}
        </td>
        `}
      </tr>
    `;
            });

            html += `
      </tbody>
    </table>
  `;

            return html;
        }
    }
    PosReceiptButton.template = 'PosReceiptButton';

    ProductScreen.addControlButton({
        component: PosReceiptButton,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(PosReceiptButton);

    return PosReceiptButton;
});
