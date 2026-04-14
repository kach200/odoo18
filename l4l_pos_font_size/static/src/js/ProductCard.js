/** @odoo-module */

import { ProductCard } from "@point_of_sale/app/generic_components/product_card/product_card";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";

patch(ProductCard.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    CardFontSize() {
        if (this.pos.config.product_font_size) {
            return `${this.pos.config.pos_font_size}px`;
        }
    },
});
