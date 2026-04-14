/** @odoo-module */

import { CategorySelector } from "@point_of_sale/app/generic_components/category_selector/category_selector";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { patch } from "@web/core/utils/patch";

patch(CategorySelector.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },

    CategoryFontSize() {
        if (this.pos.config.product_category_font_size) {
            return `${this.pos.config.pos_pro_category_font_size}px`;
        }
    },
});