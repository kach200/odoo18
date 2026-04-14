/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { Numpad } from "@point_of_sale/app/generic_components/numpad/numpad";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(Numpad.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    NumpadFontSize() {
        if (this.pos.config.pos_numpad_font_size) {
            return `${this.pos.config.pos_default_numpad_font_size}px`;
        }
    },
});