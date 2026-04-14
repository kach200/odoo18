# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    product_font_size = fields.Boolean(string="Product Card Font Size")
    pos_font_size = fields.Integer(string='Product Card Font Size', default=15)
    pos_numpad_font_size = fields.Boolean(string='Numpad Font Size')
    pos_default_numpad_font_size = fields.Integer(string='Numpad Font Size', default=15)
    customer_list_font_size = fields.Boolean(string="Customer List View Font Size")
    pos_customer_font_size = fields.Integer(string='Customer List View Font Size', default=15)
    control_button_font_size = fields.Boolean(string='Control Button Font Size')
    pos_control_buttons_font_size = fields.Integer(string='Control Button Font Size', default=15)
    sale_order_list_font_size = fields.Boolean(string='Sale Order List View Font Size')
    pos_sale_order_tree_font_size = fields.Integer(string='Sale Order List View Font Size', default=15)
    refund_button_list_font_size = fields.Boolean(string='Refund Button List View Font Size')
    pos_refund_list_view_font_size = fields.Integer(string='Refund Button List View Font Size', default=15)
    pos_order_line_font_size = fields.Boolean(string="POS Order Lines Font Size")
    order_lines_font_size = fields.Integer(string='POS Order Lines Font Size', default=15)
    payment_screen_font_size = fields.Boolean(string='Payment Screen Font Size')
    pos_payments_screen_font_size = fields.Integer(string='Payment Screen Font Size', default=15)
    receipt_screen_font_size = fields.Boolean(string='POS Receipt Screen Font Size')
    pos_receipts_screen_font_size = fields.Integer(string="POS Receipt Screen Font Size", default=15)
    product_category_font_size = fields.Boolean(string="Product Category Font Size")
    pos_pro_category_font_size = fields.Integer(string='Product Category', default=15)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    product_font_size = fields.Boolean(related='pos_config_id.product_font_size', readonly=False)
    pos_font_size = fields.Integer(related='pos_config_id.pos_font_size', readonly=False)
    pos_numpad_font_size = fields.Boolean(related='pos_config_id.pos_numpad_font_size', readonly=False, store=True)
    pos_default_numpad_font_size = fields.Integer(related='pos_config_id.pos_default_numpad_font_size', readonly=False, store=True)
    customer_list_font_size = fields.Boolean(related='pos_config_id.customer_list_font_size', readonly=False)
    pos_customer_font_size = fields.Integer(related='pos_config_id.pos_customer_font_size', readonly=False)
    control_button_font_size = fields.Boolean(related='pos_config_id.control_button_font_size', readonly=False)
    pos_control_buttons_font_size = fields.Integer(related='pos_config_id.pos_control_buttons_font_size', readonly=False)
    sale_order_list_font_size = fields.Boolean(related='pos_config_id.sale_order_list_font_size', readonly=False)
    pos_sale_order_tree_font_size = fields.Integer(related='pos_config_id.pos_sale_order_tree_font_size', readonly=False)
    refund_button_list_font_size = fields.Boolean(related='pos_config_id.refund_button_list_font_size', readonly=False)
    pos_refund_list_view_font_size = fields.Integer(related='pos_config_id.pos_refund_list_view_font_size', readonly=False)
    pos_order_line_font_size = fields.Boolean(related="pos_config_id.pos_order_line_font_size", readonly=False)
    order_lines_font_size = fields.Integer(related="pos_config_id.order_lines_font_size", readonly=False)
    payment_screen_font_size = fields.Boolean(related='pos_config_id.payment_screen_font_size', readonly=False)
    pos_payments_screen_font_size = fields.Integer(related="pos_config_id.pos_payments_screen_font_size", readonly=False)
    receipt_screen_font_size = fields.Boolean(related='pos_config_id.receipt_screen_font_size', readonly=False)
    pos_receipts_screen_font_size = fields.Integer(related='pos_config_id.pos_receipts_screen_font_size', readonly=False)
    product_category_font_size = fields.Boolean(related='pos_config_id.product_category_font_size', readonly=False)
    pos_pro_category_font_size = fields.Integer(related='pos_config_id.pos_pro_category_font_size', readonly=False)

    @api.onchange('pos_font_size', 'pos_default_numpad_font_size', 'pos_customer_font_size', 'pos_sale_order_tree_font_size', 'pos_control_buttons_font_size', 'pos_refund_list_view_font_size', 'order_lines_font_size', 'pos_payments_screen_font_size', 'pos_receipts_screen_font_size', 'pos_pro_category_font_size')
    def pos_font_size_negative(self):
        if self.pos_font_size <= 0 or self.pos_default_numpad_font_size <= 0 or self.pos_customer_font_size <= 0 or self.pos_sale_order_tree_font_size <= 0 or self.pos_control_buttons_font_size <= 0 or self.pos_refund_list_view_font_size <= 0 or self.order_lines_font_size <= 0 or self.pos_payments_screen_font_size <= 0 or self.pos_receipts_screen_font_size <= 0 or self.pos_pro_category_font_size <= 0:
            raise ValidationError('Please Enter Positive Value for Font Size')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
