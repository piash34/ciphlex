odoo.define('sh_backmate_theme_adv.custom', function (require) {
	'use strict'
	var Widget = require('web.Widget');
	var core = require('web.core');
	var config = require("web.config");

	var rpc = require('web.rpc')
	var QWeb = core.qweb;
	var _t = core._t;

	var theme_style = ''
	var sidebar_collapse_style = ''
	var search_style = ''
	rpc.query({
		model: 'sh.back.theme.config.settings',
		method: 'search_read',
		domain: [['id', '=', 1]],
		fields: ['theme_style', 'sidebar_collapse_style','search_style']
	}).then(function (data) {
		if (data) {

			if (data[0]['sidebar_collapse_style'] == 'collapsed') {
				sidebar_collapse_style = 'collapsed'
			} else {
				sidebar_collapse_style = 'expanded'
			}
			if (data[0]['search_style'] == 'collapsed') {
				search_style = 'collapsed'
			} else {
				search_style = 'expanded'
			}
			if (data[0]['theme_style'] == 'style_3') {
				theme_style = 'style_3'
			}
			else if (data[0]['theme_style'] == 'style_2') {
				theme_style = 'style_2'
			}
			else {
				theme_style = 'style_1'
			}

		}

	})


	$(document).ready(function () {

		

		$('.o_web_client').on('click', ".o_action_manager", function (ev) {

			//$('.sh_search_results').css("display","none");
			// $('.backmate_theme_layout').removeClass("sh_theme_model");
			$('.todo_layout').removeClass("sh_theme_model");
			if ($('.sh_calc_util').hasClass('active')) {
				$('.open_calc').click();
			}
			//	$('.o_action_manager').css("margin-right","0px")
			$('.sh_search_results').css("display", "none");
   
			if($('.sh_user_language_list_cls').css("display") != 'none'){
			   $('.sh_user_language_list_cls').css("display","none")
			}
			if($('.sh_wqm_quick_menu_submenu_list_cls').css("display") != 'none'){
			   $('.sh_wqm_quick_menu_submenu_list_cls').css("display","none")
			}
   
			if($('.sh_calc_util').hasClass("active")){
			   $('.sh_calc_util').removeClass("active")
			}
			
	   });
	   


		$(document).on("click", "#hide_top_bar", function () {
			$('.o_main_navbar').css("width", "0px");
			$('.o_main_navbar').css("height", "0px");
			$('.o_main_navbar').css("min-height", "0px");
			$('.o_main_navbar').css("display", "revert");
			$('.o_menu_systray').css("display", "none");


			$('body > header').css("height", "0px");
			$('.sh_search_container').css("display", "none");
			$('body > header').css("transition", "all .3s ease-out;")
			$("#show_top_bar").css("display", "block");
			$("#hide_top_bar").css("display", "none");
		});
		$(document).on("click", "#show_top_bar", function () {

			$('.o_main_navbar').css("width", "100%");
			$('.o_main_navbar').css("height", "4rem");
			$('.o_main_navbar').css("min-height", "4rem");
			$('.o_main_navbar').css("display", "flex");

			$('.o_menu_systray').attr("style", "display: inline-flex !important");

			$('.sh_search_container').css("display", "block");
			$('body > header').css("height", "auto");
			$("#hide_top_bar").css("display", "block");
			$("#show_top_bar").css("display", "none");
		});
		$(document).on("click", ".blur_div", function () {

			if ($('#js_bar_toggle_btn_mobile').css("top") != '0px') {
				if (!$('.blur_div').hasClass('blur_toggle')) {
					$('#js_bar_toggle_btn_mobile').click()
				}
			}
		});
		$(document).on("click", "#js_bar_toggle_btn_mobile", function () {

			$(".sh_backmate_theme_appmenu_div").toggleClass("sidebar_toggle");
			$(".blur_div").toggleClass("blur_toggle");
			if ($('.sidebar_toggle').css("max-width") != '100%') {
				//  $('.o_action_manager').css("margin-left" , '0px');  
				// $('.o_menu_systray').css("width", '0px');
				// $('.o_menu_systray').css("opacity", '0');
				$('ul.dropdown-menu.dropdown-menu-right').css("display", 'none');
				$('ul.dropdown-menu.dropdown-menu-right').removeClass('show_ul');
				$('span.sh_dropdown').removeClass('sh_dropdown');
				$("#toggle_bar").addClass('fa-bars');
				$("#toggle_bar").removeClass('fa-times');
				//	  $("#js_bar_toggle_btn_mobile").css("display","none");

			} else {
				// $('.o_action_manager').css("margin-left" , '310px'); 
				$('.o_menu_systray').css("width", '100%');
				$('.o_menu_systray').css("opacity", '1');
				$("#toggle_bar").removeClass('fa-bars');
				$("#toggle_bar").addClass('fa-times');
			}

		});
		$(document).on("click", "#toggle_bar", function () {
			if ($("#toggle_bar").hasClass("fa-bars")) {
				this.classList.toggle('fa-times');
				$("#toggle_bar").removeClass('fa-bars');
			} else {
				this.classList.toggle('fa-bars');
				$("#toggle_bar").removeClass('fa-times');
			}

		});
		$(document).on("click", ".o_app", function () {
			$(this).parents('.sh_dropdown_div').find('.sh_dropdown').removeClass('sh_dropdown');
			$(this).parents('.sh_dropdown_div').find('.show_ul').css("display", "none");
		});
		$(document).on("click", ".action_menu", function () {
			$('.action_menu').removeClass('active');
			$(this).parents('.dropdown-header').first().find('.action_menu').addClass('active');
			if ($('#js_bar_toggle_btn_mobile').css("top") != '0px') {
				$('#js_bar_toggle_btn_mobile').click();
			}
		});

		$(document).on("mouseover", ".sh_backmate_theme_appmenu_div", function () {

			if ($('.o_web_client').hasClass('o_rtl')) {
				if ($('#js_bar_toggle_btn_mobile').css("top") == '0px') {
					$('.o_action_manager').css("margin-right", '260px');
					$('.o_menu_systray').css("width", '260px');
					$('.o_main_navbar ul.o_menu_systray .o_debug_manager .dropdown-menu.show').css("right", "260px");
					$('.o_mail_systray_dropdown').css("right", "260px");
					$('.o_switch_company_menu .dropdown-menu').css("right", "260px");
					// $('a.child_app.o_app2.active').parents('.cssmenu').first().find('ul.dropdown-menu.dropdown-menu-right').css("display",'block');
					//   $(this).find('.o_app2.sh_dropdown.active').parents('.dropdown').find('ul.show_ul').css("display","block");
					if (sidebar_collapse_style != 'expanded' && search_style != 'collapsed') {
						$('.sh_search_input').css("margin-right", '190px');
						// $(this).find('.o_app2.sh_dropdown.active').parents('.dropdown').find('ul.show_ul').css("transition", "all 0.6s ease 0s;");
						// $(this).find('.o_app2.sh_dropdown.active').parents('.dropdown').find('ul.show_ul').slideDown("slow");
						$('#object1').css("padding-right", "0px");
					}
				}
			} else {
				if ($('#js_bar_toggle_btn_mobile').css("top") == '0px') {
					$('.o_action_manager').css("margin-left", '260px');

					$('.o_menu_systray').css("width", '260px');
					$('.o_main_navbar ul.o_menu_systray .o_debug_manager .dropdown-menu.show').css("left", "260px");
					$('.o_mail_systray_dropdown').css("left", "260px");
					$('.o_switch_company_menu .dropdown-menu').css("left", "260px");
					// $('a.child_app.o_app2.active').parents('.cssmenu').first().find('ul.dropdown-menu.dropdown-menu-right').css("display",'block');
					if (sidebar_collapse_style != 'expanded' && search_style != 'collapsed') {
						$('.sh_search_input').css("margin-left", '190px');
						// $(this).find('.o_app2.sh_dropdown.active').parents('.dropdown').find('ul.show_ul').css("transition", "all 0.6s ease 0s;");
						// $(this).find('.o_app2.sh_dropdown.active').parents('.dropdown').find('ul.show_ul').slideDown("slow");
						$('#object1').css("padding-left", "0px");
					}

					//	    	      if(theme_style == 'style_3'){
					//	    	    	  $('header').css("margin-left","190px");
					//		    	  }



				}
			}
			$(document).on("mouseover", ".o_app2.active", function () {
				$(this).parents('.sh_dropdown_div').find('ul.show_ul').css("transition", "all 0.6s ease 0s;");
				$(this).parents('.sh_dropdown_div').find('ul.show_ul').slideDown("slow");
	
				
	
			});


		});
		$(document).on("mouseleave", ".sh_backmate_theme_appmenu_div", function () {

			if ($('.o_web_client').hasClass('o_rtl')) {
				if ($('#js_bar_toggle_btn_mobile').css("top") == '0px') {

					if (sidebar_collapse_style != 'expanded') {
						$(this).find('.o_app2.sh_dropdown.active').parents('.sh_dropdown_div').find('ul.show_ul').slideUp("slow");
						$(this).find('.o_app2.sh_dropdown.active').parents('.sh_dropdown_div').find('ul.show_ul').css("transition", "all 0.6s ease 0s;");
						$('#object1').css("padding-right", "0px");
					}

					$('.o_action_manager').css("margin-right", '68px');
					$('.sh_search_input').css("margin-right", '0px');
					$('.o_menu_systray').css("width", '68px');
					if ($('ul.dropdown-menu.dropdown-menu-right').hasClass('show_ul')) {
						//$('ul.dropdown-menu.dropdown-menu-right').css("display",'none');
						//$('ul.dropdown-menu.dropdown-menu-right').removeClass('show_ul');
					}
					//$('a.child_app.o_app2.active').parents('.cssmenu').first().find('ul.dropdown-menu.dropdown-menu-right').css("display",'none');
					//	    	  		$('a.dropdown-item').removeClass('sh_sub_dropdown');
					//	    	  		$('a.dropdown-item').removeClass('active');
					//	    	  		$('a.dropdown-item').removeClass('sh_dropdown');
					$('.o_main_navbar ul.o_menu_systray .o_debug_manager .dropdown-menu.show').css("right", "68px");
					$('.o_mail_systray_dropdown').css("right", "68px");
					$('.o_switch_company_menu .dropdown-menu').css("right", "68px");
					$(this).find('.o_app2.sh_dropdown.active').parents('.sh_dropdown_div').find('ul.show_ul').css("display", "none");
				}
			} else {
				if ($('#js_bar_toggle_btn_mobile').css("top") == '0px') {

					//    		  if(theme_style == 'style_3'){
					//	    		  $('header').css("margin-left","0px");
					//	    	  }
					if (sidebar_collapse_style != 'expanded') {
						$(this).find('.o_app2.sh_dropdown.active').parents('.sh_dropdown_div').find('ul.show_ul').slideUp("slow");
						$(this).find('.o_app2.sh_dropdown.active').parents('.sh_dropdown_div').find('ul.show_ul').css("transition", "all 0.6s ease 0s;");
						$('#object1').css("padding-left", "0px");
					}

					$('.o_action_manager').css("margin-left", '68px');
					$('.sh_search_input').css("margin-left", '0px');
					$('.o_menu_systray').css("width", '68px');
					if ($('ul.dropdown-menu.dropdown-menu-right').hasClass('show_ul')) {
						//$('ul.dropdown-menu.dropdown-menu-right').css("display",'none');
						//$('ul.dropdown-menu.dropdown-menu-right').removeClass('show_ul');
					}
					//$('a.child_app.o_app2.active').parents('.cssmenu').first().find('ul.dropdown-menu.dropdown-menu-right').css("display",'none');
					//	    	  		$('a.dropdown-item').removeClass('sh_sub_dropdown');
					//	    	  		$('a.dropdown-item').removeClass('active');
					//	    	  		$('a.dropdown-item').removeClass('sh_dropdown');
					$('.o_main_navbar ul.o_menu_systray .o_debug_manager .dropdown-menu.show').css("left", "68px");
					$('.o_mail_systray_dropdown').css("left", "68px");
					$('.o_switch_company_menu .dropdown-menu').css("left", "68px");


				}


			}

		});



		$(document).on("click", ".direct_menu", function () {
			$(this).parents('.sh_dropdown_div').first().find('.active').removeClass('active');
			$(this).parents('.dropdown-menu').first().find('.active').removeClass('active');
			$(this).addClass("active")
			$(this).parents('.sh_backmate_theme_appmenu_div').find('.child_app').removeClass('focus')

		});
	// 	setTimeout(() => {
			
	// 		// $('.sh_backmate_theme_appmenu_div').addClass('sidebar_toggle')

	// 		$('.o_web_client').find('.sh_dropdown_toggle').click(function (ev) {
	// 		console.log("......",$(this))
	// 		if (!$(this).next().hasClass('show_ul')) {
	// 			$(this).next('.dropdown-menu-right').first().slideDown('slow');


	// 			$(this).parents('.dropdown-menu').first().find('.show_ul').slideUp(600)
	// 			$(this).parents('.dropdown-menu').first().find('.show_ul').css("display", "none !important")
	// 			$(this).parents('.dropdown-menu').first().find('.show_ul').removeClass('show_ul');


	// 			if ($(this).next('.dropdown-menu').parents('.dropdown-header').length == 1) {
	// 				$(this).parents('.dropdown-menu').first().find('.sh_sub_dropdown').removeClass('sh_sub_dropdown');
	// 				$(this).next('.dropdown-menu').parents('.dropdown-header').children('.dropdown-item').addClass('sh_sub_dropdown');


	// 			} else {
	// 				$(this).parents('.dropdown-menu').first().find('.sh_dropdown').removeClass('sh_dropdown');
	// 				$(this).parents('.dropdown-menu').first().find('.active').removeClass('active');

	// 				$(this).parents('.dropdown-menu').first().find('.sh_sub_dropdown').removeClass('sh_sub_dropdown');
	// 				$(this).next('.dropdown-menu').parents('.sh_dropdown_div').children('.dropdown-item').addClass('sh_dropdown');
	// 				$(this).next('.dropdown-menu').parents('.sh_dropdown_div').children('.dropdown-item').addClass('active');
	// 			}
	// 		}

	// 		if ($(this).next().hasClass('show_ul')) {
	// 			$(this).next('.dropdown-menu-right').first().slideUp(600);
	// 			//  	  	$(this).next('.dropdown-menu-right').first().css("display","none");

	// 			if ($(this).next('.dropdown-menu').parents('.dropdown-header').length == 1) {

	// 				$(this).next('.dropdown-menu').parents('.dropdown-header').children('.dropdown-item').removeClass('sh_sub_dropdown');
	// 			} else {

	// 				$(this).next('.dropdown-menu').parents('.dropdown').children('span').removeClass('sh_dropdown');
	// 				$(this).next('.dropdown-menu').parents('.dropdown').children('span').removeClass('active');
	// 			}
	// 		}

	// 		var $subMenu = $(this).next('.dropdown-menu');
	// 		$subMenu.toggleClass('show_ul');
	// 		//$subMenu.parents('.dropdown-header').children('a.dropdown-item').toggleClass('sh_sub_dropdown');
	// 		$(this).parents('.sh_backmate_theme_appmenu_div').find('.direct_menu').removeClass('focus')

	// 		$(this).parents('li.nav-item.dropdown.show_ul').on('hidden.bs.dropdown', function (e) {
	// 			$('.dropdown-submenu .show_ul').removeClass('show_ul');
	// 		});

	// 		return false;
	// 	});
	// }, 2000);

	});

});