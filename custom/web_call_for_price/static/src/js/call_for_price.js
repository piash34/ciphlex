odoo.define('call_for_price.call_for_price', function (require) {
    'use strict';
    
    var publicWidget = require('web.public.widget');

    publicWidget.registry.CallForPrice = publicWidget.Widget.extend({
        selector: '#wrapwrap',

        events: {
            'click .call_for_price_dialog_reset': '_onDialogReset',             
            'click .call_for_price_dialog_submit': '_onDialogSubmit',
            'click .call_for_price_dialog_close': '_onDialogClose',
            'click .call_for_price_dialog': '_onDialogOpen',
        },

        init: function (parent, options) {
            this.$dialog = $('#call_for_price_dialog');
            this.$form = $('#o_form_call_for_price');
            this.$success_alert = $('.call_for_price_success_alert');
            this.$danger_alert = $('.call_for_price_danger_alert');
            this._super.apply(this, arguments);
        },

        start: function(){
            this.websiteId= this.$form.find('#dialog-website-id');
            this.productId= this.$form.find('#dialog-product-id');
            this.firstName = this.$form.find('#dialog-first-name');
            this.lastName = this.$form.find('#dialog-last-name');
            this.eMail = this.$form.find('#dialog-email');
            this.phone = this.$form.find('#dialog-phone');
            this.productQty = this.$form.find('#dialog-product-qty');
            this.message = this.$form.find('#dialog-message');            
            return this._super.apply(this, arguments);
        },

        _onDialogOpen: function(ev){
            ev.preventDefault();
            if(this.$dialog){
                this.$dialog.fadeIn('slow');
            }
        },

        _onDialogClose: function(ev){
            ev.preventDefault();
            if(this.$dialog){
                this.$dialog.clearForm();
                this.$dialog.fadeOut('slow');
            }
        },

        _onDialogReset: function(ev){
            ev.preventDefault();
            if(this.$dialog){
                this.$dialog.clearForm();
                this.$success_alert.addClass('d-none');
                this.$danger_alert.addClass('d-none');
            }            
        },  

        _onDialogSubmit: function(ev){
            ev.preventDefault();
            var self = this;
            var websiteId = self.websiteId.val();
            var productId= self.productId.val();
            var firstName = self.firstName.val();
            var lastName = self.lastName.val();
            var eMail = self.eMail.val();
            var phone = self.phone.val();
            var productQty = self.productQty.val();
            var message = self.message.val();
            
            if ( productId == "" || productId == null) {
                self.productId.addClass('alert-danger');
            }
            else{
                self.productId.removeClass('alert-danger');
            }
            
            if (firstName == "") {
                self.firstName.addClass('alert-danger');
            }
            else{
                self.firstName.removeClass('alert-danger');
            }

            if (lastName == "") {
                self.lastName.addClass('alert-danger');
            }
            else{
                self.lastName.removeClass('alert-danger');
            }

            if (eMail == "") {
                self.eMail.addClass('alert-danger');
            }
            else{
                self.eMail.removeClass('alert-danger');
            }

            if (phone == "") {
                self.phone.addClass('alert-danger');
            }
            else{
                self.phone.removeClass('alert-danger');
            }

            if (productQty == "") {
                self.productQty.addClass('alert-danger');
            }
            else{
                self.productQty.removeClass('alert-danger');
            }

            if (productId && firstName && lastName && eMail && phone && productQty){
                this._rpc({
                    route: '/web_call_for_price/create_call_for_price',
                    params: {
                        'website_id': websiteId,
                        'product_id': productId,
                        'first_name': firstName,
                        'last_name': lastName,
                        'email': eMail,
                        'phone': phone,
                        'product_qty': productQty,
                        'message': message,
                    },
                }).then(function (result) {
                    console.log(result);
                    if (result.success){
                        self.$success_alert.removeClass('d-none');
                        self.$dialog.clearForm();
                    }
                    else{
                        self.$danger_alert.removeClass('d-none');
                    }                    
                    
                });
            }
        },

    });

    return {
        CallForPrice: publicWidget.registry.CallForPrice,
    };
})
