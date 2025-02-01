# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Purchase Upload Button',
    'version': '18.0.0.1',
    'category': 'Inventory/Purchase',
    'author': 'NHS',
    'summary': 'upload button in list',
    'website': 'www.syrupsbiz.com',
    'description': """
extends existing js_class and upload button in list
    """,
    'depends': ['purchase'],
    'data': [
        'views/purchase_order_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'upload_button/static/src/js/upload_button.js',
            'upload_button/static/src/xml/upload_button_view.xml',
        ],
    },
    'images':  ['static/description/image_1.jpg'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}
