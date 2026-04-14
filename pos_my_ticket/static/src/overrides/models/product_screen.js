/** @odoo-module **/

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";
import { patch } from "@web/core/utils/patch";

patch(OrderWidget.prototype, {
    _getCurrentOrder() {
        return (
            this.props?.order ||
            this.props?.selectedOrder ||
            this.props?.ticketOrder ||
            this.props?.activeOrder ||
            this.props?.selected_order ||
            this.pos?.get_order?.() ||
            this.env?.services?.pos?.get_order?.() ||
            null
        );
    },

    _getOrderLines() {
        const directLines =
            this.props?.lines ||
            this.props?.orderlines ||
            this.props?.selectedOrder?.lines ||
            this.props?.ticketOrder?.lines ||
            this.props?.activeOrder?.lines ||
            this.props?.selected_order?.lines ||
            null;

        if (Array.isArray(directLines)) {
            return directLines;
        }

        if (typeof directLines === "function") {
            const evaluated = directLines();
            if (Array.isArray(evaluated)) {
                return evaluated;
            }
        }

        const order = this._getCurrentOrder();
        if (order?.get_orderlines) {
            return order.get_orderlines();
        }

        if (Array.isArray(order?.lines)) {
            return order.lines;
        }

        return [];
    },

    get ItemCount() {
        return this._getOrderLines().length;
    },

    get TotalQuantity() {
        return this._getOrderLines().reduce((total, line) => {
            const qty =
                (typeof line.get_quantity === "function" && line.get_quantity()) ||
                (typeof line.qty === "function" && line.qty()) ||
                line.quantity ||
                line.qty_to_refund ||
                line.qty ||
                0;
            return total + Number(qty || 0);
        }, 0);
    }
});