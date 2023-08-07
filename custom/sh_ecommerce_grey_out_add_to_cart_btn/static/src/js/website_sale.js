odoo.define('sh_ecommerce_grey_out_add_to_cart_btn.website_sale', function (require) {
'use strict';
require('website_sale.website_sale');

var publicWidget = require('web.public.widget');
var WebsiteSale = require('website_sale.website_sale');
	
	publicWidget.registry.WebsiteSale.include({

    events: _.extend({}, publicWidget.registry.WebsiteSale.prototype.events, {
    }),
	//--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------
		/**
	     * @override
	     */
		start() {
			$(".is_cart_grey_out_cls_uniq_grey").popover({ trigger: "hover" })
			$(".is_rfq_grey_out_cls_uniq_grey").popover({ trigger: "hover" })
			return this._super(...arguments);
		},
	});
});