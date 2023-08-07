# Part of Softhealer Technologies.
{
    "name": "Disable Add to Cart Button",
    "author": "Softhealer Technologies",
    "support": "support@softhealer.com",
    "website": "https://www.softhealer.com",
    "category": "Website",
    "license": "OPL-1",
    "summary": "Ecommerce Grey Out Add to cart Button Disable Cart Button Temporary Remove Cart Button Hide Cart Button Stop Add To Cart Disable Odoo",
    "description": """This module helps to disable add to cart button for all products from shop. You can disable add to cart button for public user, who dont login in to the website.""",
    "version": "16.0.1",
    "depends": ['website_sale_wishlist','website_sale_comparison'],
    "data": [
            'views/website_sale_templates.xml',
            'views/website_views.xml',
    ],
   'assets': {
        'web.assets_frontend': [
            'sh_ecommerce_grey_out_add_to_cart_btn/static/src/js/website_sale.js',
            'sh_ecommerce_grey_out_add_to_cart_btn/static/src/scss/shop.scss',
        ],
    },
    "images": ['static/description/background.png', ],
    "auto_install": False,
    "application": True,
    "installable": True,
    "price": 15,
    "currency": 'EUR',
}
