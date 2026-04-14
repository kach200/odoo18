/** @odoo-module */

import { PartnerList } from "@point_of_sale/app/screens/partner_list/partner_list";
import { patch } from "@web/core/utils/patch";
import { usePos } from "@point_of_sale/app/store/pos_hook";

patch(PartnerList.prototype, {
    setup() {
        super.setup();
        this.pos = usePos();
    },
    CustomerListViewFontSize() {
        if (this.pos.config.customer_list_font_size) {
            return `${this.pos.config.pos_customer_font_size}px`;
        }
    },
});