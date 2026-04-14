/** @odoo-module */

import { PaymentScreen } from "@point_of_sale/app/screens/payment_screen/payment_screen";
import { patch } from "@web/core/utils/patch";

patch(PaymentScreen.prototype, {
    setup() {
        super.setup(...arguments);
        },
        POSPaymentScreenFontSize() {
        if (this.pos.config.payment_screen_font_size) {
            return `${this.pos.config.pos_payments_screen_font_size}px`;
        }
    },
});
