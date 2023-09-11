/** @odoo-module **/
import { MenuDropdown, MenuItem, NavBar } from '@web/webclient/navbar/navbar';
import { patch } from 'web.utils';
// import { ProfileSection } from "@sh_backmate_theme/js/profilesection";
import { ErrorHandler, NotUpdatable } from "@web/core/utils/components";

const components = { NavBar };
var rpc = require("web.rpc");

var theme_style = 'default';

var config = require("web.config");
var session = require('web.session');
var rpc = require('web.rpc')
var icon_style = 'standard';


rpc.query({
    model: 'sh.back.theme.config.settings',
    method: 'search_read',
    args: [[], ['icon_style']],
}, { async: false }).then(function (output) {
    if (output) {
        var i;
        for (i = 0; i < output.length; i++) {
            if (output[i]['icon_style']) {
                icon_style = output[i]['icon_style'];
            }

        }
    }
});


// console.log(" NavBar.components", NavBar.components)

// NavBar.components = { MenuDropdown, MenuItem, NotUpdatable, ErrorHandler, ProfileSection };
// console.log(" NavBar.components", NavBar.components)
patch(components.NavBar.prototype, 'sh_backmate_theme_adv/static/src/js/navbar.js', {

    //--------------------------------------------------------------------------
    // Public
    //--------------------------------------------------------------------------

    /**
     * @override
     */

    // mobileNavbarTabs(...args) {
    //     return [...this._super(...args), {
    //         icon: 'fa fa-comments',
    //         id: 'livechat',
    //         label: this.env._t("Livechat"),
    //     }];
    // }



    // onNavBarDropdownItemSelection(ev) {
    //     const { payload: menu } = ev.detail;
    //     if (menu) {
    //         this.menuService.selectMenu(menu);
    //         // $("body").removeClass("sh_sidebar_background_enterprise");
    //         // $(".sh_search_container").css("display", "none");
    //         // $(".sh_backmate_theme_appmenu_div").removeClass("show")
    //         // $(".o_action_manager").removeClass("d-none");
    //         // $(".o_menu_brand").css("display", "block");
    //         // $(".full").removeClass("sidebar_arrow");
    //         // $(".o_menu_sections").css("display", "flex");


    //     }
    // },
    get_current_company(){
        let current_company_id;
        if (session.user_context.allowed_company_ids) {
            current_company_id = session.user_context.allowed_company_ids[0];
        } else {
            current_company_id = session.user_companies ?
                session.user_companies.current_company :
                false;
        }

        return current_company_id;
    },
    getIconStyle() {
        return icon_style;
    },
    getAppClassName(app){
        var app_name = app.xmlid
        return app_name.replaceAll('.', '_')
    },
    getXmlID(app_id) {
        return this.menuService.getMenuAsTree(app_id).xmlid;
    },
    OnClickDropdown(ev){

			if (!$(ev.currentTarget).next().hasClass('show_ul')) {
				$(ev.currentTarget).next('.dropdown-menu-right').first().slideDown('slow');


				$(ev.currentTarget).parents('.dropdown-menu').first().find('.show_ul').slideUp(600)
				$(ev.currentTarget).parents('.dropdown-menu').first().find('.show_ul').css("display", "none !important")
				$(ev.currentTarget).parents('.dropdown-menu').first().find('.show_ul').removeClass('show_ul');


				if ($(ev.currentTarget).next('.dropdown-menu').parents('.dropdown-header').length == 1) {
					$(ev.currentTarget).parents('.dropdown-menu').first().find('.sh_sub_dropdown').removeClass('sh_sub_dropdown');
					$(ev.currentTarget).next('.dropdown-menu').parents('.dropdown-header').children('.dropdown-item').addClass('sh_sub_dropdown');


				} else {
					$(ev.currentTarget).parents('.dropdown-menu').first().find('.sh_dropdown').removeClass('sh_dropdown');
					$(ev.currentTarget).parents('.dropdown-menu').first().find('.active').removeClass('active');

					$(ev.currentTarget).parents('.dropdown-menu').first().find('.sh_sub_dropdown').removeClass('sh_sub_dropdown');
					$(ev.currentTarget).next('.dropdown-menu').parents('.sh_dropdown_div').children('.dropdown-item').addClass('sh_dropdown');
					$(ev.currentTarget).next('.dropdown-menu').parents('.sh_dropdown_div').children('.dropdown-item').addClass('active');
				}
			}

			if ($(ev.currentTarget).next().hasClass('show_ul')) {
				$(ev.currentTarget).next('.dropdown-menu-right').first().slideUp(600);
				//  	  	$(this).next('.dropdown-menu-right').first().css("display","none");

				if ($(ev.currentTarget).next('.dropdown-menu').parents('.dropdown-header').length == 1) {
					$(ev.currentTarget).next('.dropdown-menu').parents('.dropdown-header').children('.dropdown-item').removeClass('sh_sub_dropdown');
				} else {

                    console.log(".....................",$(ev.currentTarget).next('.dropdown-menu') )
					$(ev.currentTarget).next('.dropdown-menu').parents('.sh_dropdown_div').children('span').removeClass('sh_dropdown');
					$(ev.currentTarget).next('.dropdown-menu').parents('.sh_dropdown_div').children('span').removeClass('active');
				}
			}

			var $subMenu = $(ev.currentTarget).next('.dropdown-menu');
			$subMenu.toggleClass('show_ul');
			// //$subMenu.parents('.dropdown-header').children('a.dropdown-item').toggleClass('sh_sub_dropdown');
			// $(ev.currentTarget).parents('.sh_backmate_theme_appmenu_div').find('.direct_menu').removeClass('focus')

			// $(ev.currentTarget).parents('li.nav-item.dropdown.show_ul').on('hidden.bs.dropdown', function (e) {
			// 	$('.dropdown-submenu .show_ul').removeClass('show_ul');
			// });


    },
    currentMenuAppSections(app_id) {

        return (
            (this.menuService.getMenuAsTree(app_id).childrenTree) ||
            []
        );
    },



    getThemeStyle(ev) {

        return theme_style;
    },
    isMobile(ev) {
        return config.device.isMobile;
    },
    click_secondary_submenu(ev) {
        if (config.device.isMobile) {
            $(".sh_sub_menu_div").addClass("o_hidden");
        }

        $(".o_menu_sections").removeClass("show")
    },
    click_close_submenu(ev) {
        $(".sh_sub_menu_div").addClass("o_hidden");
        $(".o_menu_sections").removeClass("show")
    },
    click_mobile_toggle(ev) {
        $(".sh_sub_menu_div").removeClass("o_hidden");

    },
    // click_app_toggle(ev) {
    //     console.log(">>>>>>>>>>>>h_backmate_theme_appmenu_div", $(".sh_backmate_theme_appmenu_div"))
    //     if ($(".sh_backmate_theme_appmenu_div").hasClass("show")) {
    //         $("body").removeClass("sh_sidebar_background_enterprise");
    //         $(".sh_search_container").css("display", "none");

    //         $(".sh_backmate_theme_appmenu_div").removeClass("show")
    //         $(".o_action_manager").removeClass("d-none");
    //         $(".o_menu_brand").css("display", "block");
    //         $(".full").removeClass("sidebar_arrow");
    //         $(".o_menu_sections").css("display", "flex");
    //     } else {
    //         $(".sh_backmate_theme_appmenu_div").addClass("show")
    //         $("body").addClass("sh_sidebar_background_enterprise");
    //         $(".sh_backmate_theme_appmenu_div").css("opacity", "1");
    //         //$(".sh_search_container").css("display","block");
    //         $(".o_action_manager").addClass("d-none");
    //         $(".full").addClass("sidebar_arrow");
    //         $(".o_menu_brand").css("display", "none");
    //         $(".o_menu_sections").css("display", "none");
    //     }


    // },


});


