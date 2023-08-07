from odoo import http
from odoo import api, fields, models, _
from odoo.http import request
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.website_sale.controllers.main import WebsiteSale

class CallForPriceDialog(http.Controller):
    @http.route(['/web_call_for_price/create_call_for_price'], type='json', auth='public', methods=['POST'])
    def call_for_price(self, website_id, product_id, first_name, last_name, email, phone, product_qty, message, **kw):
        website = request.env['website'].sudo().search([('id', '=', int(website_id))])
        if product_id and first_name and last_name and email and phone and product_qty:
            values = {
                'product_id' : product_id,
                'first_name' : first_name,
                'last_name' : last_name,
                'email' : email,
                'phone' : phone,
                'product_qty' : product_qty,
                'message' : message,
                'website_id': website.id,
                'company_id': website.company_id.id,
                }
            call_for_price = request.env['call.for.price'].sudo().create(values)
            if call_for_price:
                return {'success': _('Your Call for Price request has been generated.')}
            else:
                return {'errors': _('Something went wrong during your request generation.')}
        else:
            return {'errors': _('Something went wrong during your request generation.')}

class WebsiteSale(WebsiteSale):
    def _get_products_recently_viewed(self):
        """
        Returns list of recently viewed products according to current user
        """
        max_number_of_product_for_carousel = 12
        visitor = request.env['website.visitor']._get_visitor_from_request()
        if visitor:
            excluded_products = request.website.sale_get_order().mapped('order_line.product_id.id')
            products = request.env['website.track'].sudo().read_group(
                [('visitor_id', '=', visitor.id), ('product_id', '!=', False),
                ('product_id.website_published', '=', True), ('product_id', 'not in', excluded_products)],
                ['product_id', 'visit_datetime:max'], ['product_id'], limit=max_number_of_product_for_carousel, orderby='visit_datetime DESC')
            products_ids = [product['product_id'][0] for product in products]
            
            if products_ids:
                viewed_products = request.env['product.product'].with_context(display_default_code=False).browse(products_ids)
                FieldMonetary = request.env['ir.qweb.field.monetary']
                monetary_options = {
                    'display_currency': request.website.get_current_pricelist().currency_id,
                    }
                rating = request.website.viewref('website_sale.product_comment').active
                res = {'products': []}
                
                for product in viewed_products:
                    call_for_price_settings = product.product_tmpl_id.get_call_for_price_settings(request.website.id)
                    if call_for_price_settings:
                        continue
                    combination_info = product._get_combination_info_variant()
                    res_product = product.read(['id', 'name', 'website_url'])[0]
                    res_product.update(combination_info)
                    res_product['price'] = FieldMonetary.value_to_html(res_product['price'], monetary_options)
                    if rating:
                        res_product['rating'] = request.env["ir.ui.view"]._render_template('portal_rating.rating_widget_stars_static', values={
                            'rating_avg': product.rating_avg,
                            'rating_count': product.rating_count,
                            })
                    res['products'].append(res_product)
                    
                return res
        return {}