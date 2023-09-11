# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
{
    "name": "Backmate Backend Theme Advance - Compatibility With Frontend",
    "author": "Softhealer Technologies",
    "website": "https://www.softhealer.com",
    "support": "support@softhealer.com",
    "description": """Here in this theme, we provide 4 different well-crafted login styles for desktop and mobile views. You can use these styles on the website. Also, you can set the display company icon/logo on the login screen.""",
    "summary": "Advance Material Backend Theme Responsive Theme Fully functional Theme flexible Backend Theme fast Backend Theme lightweight Backend Theme Animated Backend Theme Modern Login Style Login Page Login Theme Ciphlex",
    "category": "Extra Tools",
    "license": "OPL-1",
    "version": "16.0.1",
    "depends":
    [
        "sh_backmate_theme_adv", "website"
    ],

    "data":
    [
       "views/login_layout.xml"
    ],
     'assets': {
          'web.assets_frontend': [
            'sh_backmate_adv_website_login/static/src/scss/login_page/login_style_1.scss',
            'sh_backmate_adv_website_login/static/src/scss/login_page/login_style_2.scss',
            'sh_backmate_adv_website_login/static/src/scss/login_page/login_style_3.scss',
            'sh_backmate_adv_website_login/static/src/scss/login_page/login_style_4.scss'
           
        ],
  
    },
    "live_test_url": "https://softhealer.com/contact_us",
    "installable": True,
    "application": True,
    "images": ["static/description/background.png", ],
    "price": 10,
    "currency": "EUR",
    "bootstrap": True,

}
