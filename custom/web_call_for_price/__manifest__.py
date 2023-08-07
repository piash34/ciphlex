# -*- coding: utf-8 -*-
#################################################################################
# Author      : CFIS (<https://www.cfis.store/>)
# Copyright(c): 2017-Present CFIS.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://www.cfis.store/>
#################################################################################

{
    "name": "Call For Price  - Website Request a Call for Price",
    "summary": "This module allows you to activate a call for price and hide the product price, as well as add a call for price button. The customer presses the button to submit the merchant a price request.",
    "version": "16.0.1",
    "description": """
        This module allows you to activate a call for price and hide the product price, as well as add a call for price button. The customer presses the button to submit the merchant a price request.      
    """,    
    "author": "CFIS",
    "maintainer": "CFIS",
    "license" :  "Other proprietary",
    "website": "https://www.cfis.store",
    "images": ["images/web_call_for_price.png"],
    "category": "eCommerce",
    "depends": [
        "website_sale",
        "sale_management",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/call_for_price_views.xml",
        "views/res_config_settings_views.xml",
        "views/product.xml",
        "views/website_templates.xml",
        "wizard/call_for_price_settings_wizard_views.xml"
    ],
    "assets": {
        "web.assets_frontend": [
            "/web_call_for_price/static/src/js/call_for_price.js",
        ],
        "web.assets_qweb": [],
    },    
    "installable": True,
    "application": True,
    "price"                 :  16.00,
    "currency"              :  "EUR",
    "pre_init_hook"         :  "pre_init_check",
}
