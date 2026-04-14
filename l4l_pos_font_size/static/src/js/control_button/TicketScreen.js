/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(TicketScreen.prototype, {
    setup() {
        super.setup(...arguments);
        this.pos = usePos();
    },
    ControlButtons() {
        if (this.pos.config.control_button_font_size) {
            return `${this.pos.config.pos_control_buttons_font_size}px`;
        }
    },
});