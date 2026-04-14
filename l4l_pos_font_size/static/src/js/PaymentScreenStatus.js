/** @odoo-module */

import { PaymentScreenStatus } from "@point_of_sale/app/screens/payment_screen/payment_status/payment_status";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(PaymentScreenStatus.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
        },
        POSPaymentScreenFontSize() {
        if (this.pos.config.payment_screen_font_size) {
            return `${this.pos.config.pos_payments_screen_font_size}px`;
        }
    },
});