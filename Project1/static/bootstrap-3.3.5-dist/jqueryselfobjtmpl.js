//jquery自定义对象的模板
(function(){
	$.jqueryself = function(){};
	$.extend($.jqueryself,{
		//静态属性
		a1:'11'
	},{
		//静态方法
		fn1:function(){
			
		},
		
		fn2:function(){
			
		}
	});
})(jQuery);