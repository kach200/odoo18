/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";
import { ListRenderer } from "@web/views/list/list_renderer";


patch(ListRenderer.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    SaleOrderFontSize() {
        if (this.pos.config.sale_order_list_font_size) {
            return `${this.pos.config.pos_sale_order_tree_font_size}px`;
        }
    },
});