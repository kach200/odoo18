/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";

patch(ActionpadWidget.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    CustomerButtonFontSize() {
        if (this.pos.config.control_button_font_size) {
            return `${this.pos.config.pos_control_buttons_font_size}px`;
        }
    },
});