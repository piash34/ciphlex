from odoo import api, models, fields, tools, _

class CallForPriceSettingsWizard(models.TransientModel):
    _name = 'call.for.price.settings.wizard'
    _description = 'Update Call for Price'
    
    call_for_price_settings = fields.Boolean("Call For Price", default=False, help='Allow for a price request for products based on the selection.')

    def update_call_for_price(self):
        self.env['product.template'].browse(self.env.context.get('active_ids')).sudo().write({
            'call_for_price_settings': self.call_for_price_settings
            })    