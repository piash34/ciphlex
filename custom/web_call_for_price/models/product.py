from odoo import api, models, fields, tools, _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    call_for_price_settings = fields.Boolean(string="Call For Price", default=False, help="Allow for a price request for products based on the selection.")

    def get_call_for_price_settings(self, website_id):
        self.ensure_one()
        if self.call_for_price_settings:
            return self.call_for_price_settings            
        else:
            if website_id:
                return self.env['website'].sudo().search([('id','=',website_id)]).call_for_price_settings
        return 'show'