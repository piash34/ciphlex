from odoo import api, fields, models, _

class CallForPrice(models.Model):
    _name = 'call.for.price'
    _rec_name = 'name'
    _order = 'id'
    _description = 'Call for Price'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'website.seo.metadata', 'website.published.mixin']

    name = fields.Char('Reference', required=True,  copy=False, readonly=True, index=True, default=lambda self: _('New'))
    website_id = fields.Many2one('website', string="website", ondelete='cascade')
    first_name = fields.Char('First Name',copy=False)
    last_name = fields.Char('Last Name',copy=False)
    email = fields.Char('Email',copy=False)
    phone = fields.Char('Phone', copy=False)
    company_id = fields.Many2one('res.company', string="Company")
    product_id = fields.Many2one('product.product', required=True, string='Product',copy=False)
    product_qty = fields.Float('Quantity', default=1.0, digits='Unit of Measure', required=True, copy=False)
    message = fields.Text(string='Message', copy=False)
    image = fields.Image(related='product_id.image_1920',readonly=True)

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('call.for.price') or _('New')
        result = super(CallForPrice, self).create(vals)
        return result