/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(ProductScreen.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    ControlButtons() {
        if (this.pos.config.control_button_font_size) {
            return `${this.pos.config.pos_control_buttons_font_size}px`;
        }
    },
});