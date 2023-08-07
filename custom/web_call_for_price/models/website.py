from odoo import fields, models, api, _

class Website(models.Model):
    _inherit = 'website'

    call_for_price_settings = fields.Boolean("Call For Price", help='By enabling this option, you can enable Call for Price for all Products globally.')