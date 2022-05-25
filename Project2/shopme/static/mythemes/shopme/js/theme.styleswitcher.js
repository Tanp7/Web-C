;(function(){
	"use strict";

	var switcher = {

		BODY : $('body'),
		LAYOUT : $('.boxed_layout,.wide_layout'),
		COLOR : $('.sw_section.bg_color'),
		IMAGES : $('.sw_section.bg_images'),
		BGCHANGE : $('#bg_change_select'),
		LAYOUTBUTTONS : $('[data-layout]'),
		HEADER : $('#header'),
		FOOTER : $('#footer'),

		init : function(){

			this.colorPicker();
			this.layoutChange();
			this.bgSelect();
			this.reset();
			this.headerTypeChange();
			this.footerTypeChange();

		},

		colorPicker : function(){

			var sc = $('#change_bg_color'),
				self = this;

			sc.ColorPicker({
				color: '#004969',
				onShow: function (colpkr){
					$(colpkr).fadeIn(500);
					return false;
				},
				onHide: function (colpkr) {
					$(colpkr).fadeOut(500);
					return false;
				},
				onChange: function (hsb, hex, rgb){
					self.BODY.css('background-image','none');
					sc.add(self.BODY).css('backgroundColor', '#' + hex);
				}
			});

		},

		layoutChange : function(){

			var self = this;

			self.LAYOUTBUTTONS.on('click', function(){

				var l = $(this).data('layout');
				$(this).addClass('active').siblings().removeClass('active');

				if(l == "wide"){
					self.LAYOUT.removeClass('boxed_layout').addClass('wide_layout');
				}
				else{
					self.LAYOUT.removeClass('wide_layout').addClass('boxed_layout');	
				}

			});	

		},

		bgSelect : function(){
			var self = this;

			self.BGCHANGE.find('.options_list').on('click', 'li', function(){

				var bg = $(this).text();

				if(bg === "Color"){
					self.IMAGES.slideUp(function(){
						self.COLOR.slideDown();
					});
				}
				else{
					self.COLOR.slideUp(function(){
						self.IMAGES.slideDown();
					});
				}

			});

			$('.bg_images .change_bg').each(function(){
				$(this).css('background-image','url('+$(this).data('src')+')');
			}).on('click', function(){
				self.BODY.css('background-image','url('+$(this).data('src')+')');
			});

		},

		reset : function(){

			var self = this;

			$('#sw_reset').on('click', function(){

				self.BODY.css({
					'background-color' : '#004969',
					'background-image' : 'none'
				});

				self.LAYOUT.removeClass('boxed_layout').addClass('wide_layout');

				self.LAYOUTBUTTONS.removeClass('active').eq(0).addClass('active');

				self.BGCHANGE.children('.active_option').text("Color");

				self.IMAGES.slideUp(function(){
					self.COLOR.slideDown();
				});


			});

		},

		headerTypeChange : function(){

			var self = this;

			$('#change_header_type').children('.options_list').children(':first').children('a').addClass('active');

			$('#change_header_type').on('click', 'a:not(.active)', function(){
				
				var $this = $(this),
					url,
					type = "";

					$this.addClass('active').parent().siblings().children('a').removeClass('active');

				switch($this.text()){

					case "Header 1" :
						url = "inc/header_1.html";
						type = 'type_6';
					break;

					case "Header 2" :
						url = "inc/header_2.html";
						type = 'type_2';
					break;

					case "Header 3" :
						url = "inc/header_3.html";
					break;

					case "Header 4" :
						url = "inc/header_4.html";
						type = 'type_4';
					break;

					case "Header 5" :
						url = "inc/header_5.html";
						type = 'type_5';
					break;

					case "Header 6" :
						url = "inc/header_6.html";

				}

				self.HEADER.slideUp(function(){

					self.HEADER.removeClass('type_1 type_2 type_3 type_4 type_5 type_6').addClass(type);

					$(this).load(url, function(data){

						$(this).slideDown(function(){

							$(this).find('.dropdown').each(function(){

								Core.mainAnimation.prepareDropdown.call($(this));

							});

							// if($('#main_navigation_wrap').length){

								Core.stickyMenu.initVars();
								Core.stickyMenu.destroy();
								Core.stickyMenu.initVars();
								
							// }

						});

					});

				});

			});

		},

		footerTypeChange : function(){

			var self = this;

			$('#change_footer_type').children('.options_list').children(':first').children('a').addClass('active');

			$('#change_footer_type').on('click', 'a:not(.active)', function(){
				
				var $this = $(this),
					url,
					type = "";

					$this.addClass('active').parent().siblings().children('a').removeClass('active');

				switch($this.text()){

					case "Footer 1" :
						url = "inc/footer_1.html";
					break;

					case "Footer 2" :
						url = "inc/footer_2.html";
						type = 'type_2';
					break;

					case "Footer 3" :
						url = "inc/footer_3.html";
					break;

					case "Footer 4" :
						url = "inc/footer_4.html";
						type = 'type_4';
					break;

					case "Footer 5" :
						url = "inc/footer_5.html";
						type = 'type_5';
					break;

					case "Footer 6" :
						url = "inc/footer_6.html";
						type = 'type_6';

				}

				self.FOOTER.slideUp(function(){

					$(this).load(url, function(data){

						$(this).slideDown(function(){

							self.FOOTER.removeClass('type_1 type_2 type_3 type_4 type_5 type_6').addClass(type);

							if(self.FOOTER.find('.tweet_list_wrap').length){

								self.FOOTER.find('.tweet_list_wrap').tweet(window.twitterConfig);
								$('.twitter_follow').attr({
									'href' : 'http://www.twitter.com/' + window.twitterConfig.username,
									'target' : '_blank'
								});

							}

							$('html, body').animate({
								scrollTop : $(document).height()
							});

						});

					});

				});

			});

		}


	}

	
	$(window).load(function(){
		switcher.init();
	});	

}());