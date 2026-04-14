/** @odoo-module */

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";


patch(OrderWidget.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    POSOrderLineFontSize() {
        if (this.pos.config.pos_order_line_font_size) {
            return `${this.pos.config.order_lines_font_size}px !important`;
        }
    },
});