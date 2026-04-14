/** @odoo-module */

import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(TicketScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    RefundTicketScreenFontSize() {
        if (this.pos.config.refund_button_list_font_size) {
            return `${this.pos.config.pos_refund_list_view_font_size}px`;
        }
    },
});