from odoo import fields, models, api, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    call_for_price_settings = fields.Boolean(related='website_id.call_for_price_settings', 
        readonly=False, help='By enabling this option, you can enable Call for Price for all Products globally.')