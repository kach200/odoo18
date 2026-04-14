/** @odoo-module */

import { OrderReceipt } from "@point_of_sale/app/screens/receipt_screen/receipt/order_receipt";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(OrderReceipt.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },
    ReceiptScreenFontSize() {
        if (this.pos.config.receipt_screen_font_size) {
            return `${this.pos.config.pos_receipts_screen_font_size}px !important`;
        }
    },
});