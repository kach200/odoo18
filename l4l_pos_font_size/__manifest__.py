# -*- coding: utf-8 -*-
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2023 Leap4Logic Solutions PVT LTD
#    Email : sales@leap4logic.com
#################################################

{
    'name': "POS Font Size",
    'category': 'Point Of Sales',
    'version': '18.0.1.0',
    'sequence': 5,
    'summary': """POS Product Font Size, POS Product Card Font Resize, POS Font Resize, POS Font Size Set Dynamic, POS Font Size, POS Product Font Resize, POS Font Size, POS Order Line Font Size, POS Numpad Font Size, POS Customer Button Font Size, POS Control Button Font Size, POS Customer List View Font Size, POS Refund Button List View Font Size, POS Ticket Screen Font Size, POS Payment Screen Font Size, POS Receipt Screen Font Size, Font Size, Font, Size""",
    'description': """This Plugin Enables Users to Adjust the Font Size of Products Within the POS System.""",
    'author': 'Leap4Logic Solutions Private Limited',
    'website': 'https://leap4logic.com/',
    'depends': ['base', 'point_of_sale', 'pos_sale', 'web'],
    'data': [
        'views/pos_res_config_setting_view.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'l4l_pos_font_size/static/src/js/ProductCard.js',
            'l4l_pos_font_size/static/src/js/Numpad.js',
            'l4l_pos_font_size/static/src/js/PartnerListScreen.js',
            'l4l_pos_font_size/static/src/js/control_button/ProductScreen.js',
            'l4l_pos_font_size/static/src/js/control_button/TicketScreen.js',
            # 'l4l_pos_font_size/static/src/js/control_button/CustomerButton.js',
            'l4l_pos_font_size/static/src/js/SaleOrderList.js',
            'l4l_pos_font_size/static/src/js/RefundButtonListView.js',
            'l4l_pos_font_size/static/src/js/POSOrderLine.js',
            'l4l_pos_font_size/static/src/js/PaymentScreen.js',
            'l4l_pos_font_size/static/src/js/PaymentScreenStatus.js',
            'l4l_pos_font_size/static/src/js/PaymentScreenPaymentLines.js',
            'l4l_pos_font_size/static/src/js/ReceiptScreen.js',
            'l4l_pos_font_size/static/src/js/OrderReceipt.js',
            'l4l_pos_font_size/static/src/js/CategorySelector.js',

            'l4l_pos_font_size/static/src/xml/ProductCard.xml',
            'l4l_pos_font_size/static/src/xml/Numpad.xml',
            'l4l_pos_font_size/static/src/xml/PartnerListScreen.xml',
            'l4l_pos_font_size/static/src/xml/ControlButton.xml',
            'l4l_pos_font_size/static/src/xml/SaleOrderList.xml',
            'l4l_pos_font_size/static/src/xml/RefundButtonListView.xml',
            'l4l_pos_font_size/static/src/xml/POSOrderLine.xml',
            'l4l_pos_font_size/static/src/xml/PaymentScreen.xml',
            'l4l_pos_font_size/static/src/xml/ReceiptScreen.xml',
            'l4l_pos_font_size/static/src/xml/ProductCategory.xml',

            'l4l_pos_font_size/static/src/css/control_button_btn.css',
            'l4l_pos_font_size/static/src/css/order_line_total_fs.css',
            'l4l_pos_font_size/static/src/css/payment_screen_btn.css',
            'l4l_pos_font_size/static/src/css/receipt_screen_btn.css',
            'l4l_pos_font_size/static/src/css/product_screen.css',
        ],
    },
    'installable': True,
    'application': True,
    'images': ['static/description/banner.gif'],
    'license': 'OPL-1',
    'price': '15.99',
    'currency': 'USD',
    'live_test_url': 'https://youtu.be/m6sZVMYiHVE',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
