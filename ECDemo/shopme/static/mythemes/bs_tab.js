/*
options:
ulId: tab标签页所在的容器，ul，默认：myTab
divId: 内容所在的容器，div，默认：myTabContent

name: 当前tab的名称
title: 当前tab的标题
closable: 是否允许关闭，默认是true
content: 直接的html内容
url:当前tab所指向的URL地址，需要使用iframe，前提是content未指定
confirm: 关闭的时候是否提示，默认true
active: 新增的时候是否激活，默认true
callback: 回调函数，最后都添加之后的处理
*/

var default_tab_ul_id = 'myTab';
var default_tab_div_id = 'myTabContent';
//iframe的高度需要减去的
var topHeight = 55;

//关闭标签卡的动作
var close_action = function(tabname){
	//如果关闭的是当前激活的TAB，激活他的前一个TAB
	if($('#tab_li_'+tabname).hasClass('active')){
		var prev = $('#tab_li_'+tabname).prev();
		if(prev.length>0){
			var a = prev.children();
			prev.addClass('active');
			$(a.attr('href')).addClass('active in');
		}
	}
    
    //关闭TAB
    $("#tab_li_" + tabname).remove();
    $("#tab_content_" + tabname).remove();
};

//删除一个tab
var closeTab = function(tabname,closeConfirm){
	if(typeof(closeConfirm)=='boolean' && closeConfirm){
		
		swal({
			title:'确实要关闭标签卡吗？',
			//text:'确实要退出吗？',
			icon:'info',
			closeOnClickOutside:true,
			closeOnEsc:true,
			buttons:['取消','确定']
		}).then(function(value){
			if(value==null)
				return;
			
			close_action(tabname);
		});
		
	}else{
		close_action(tabname);
	}
};


//添加一个tab
var addTab = function(options){
	if(typeof(options) != 'object'){
		alert('参数options必须是一个object');
		return;
	}
		
	if(typeof(options.name) != 'string'){
		alert('必要包含类型为string的属性: name');
		return;
	}
		
	
	var ulId = typeof(options.ulId)=='string'?options.ulId:default_tab_ul_id;
	var divId = typeof(options.divId)=='string'?options.divId:default_tab_div_id;
	
	var exist = $("#"+ulId+" > #tab_li_"+options.name).length>0?true:false;
	
	if(exist){
		//已经存在了，直接出发点击事件
		$("#tab_a_"+options.name).click();
		return;
	}
	
	//不存在，则新增
	//首先在ul里面增加li内容的
	var title = typeof(options.title)=='string'?options.title:options.name;
	var closable = typeof(options.closable)=='boolean'?options.closable:true;
	
	var html_ul = '<li id="tab_li_'+options.name+'">';
	html_ul += '<a href="#tab_content_'+options.name+'" data-toggle="tab" id="tab_a_'+options.name+'">';
	html_ul += title;
	if(closable){
		var closeConfirm = typeof(options.confirm)=='boolean'?options.confirm:true;
		html_ul += '&nbsp;<button type="button" class="btn btn-default btn-link btn-xs" onclick="closeTab(\''+options.name+'\','+closeConfirm+')"><span class="glyphicon glyphicon-remove"></span></button>';
	}
	html_ul +='</a></li>';
	
	//添加到ul中
	$('#'+ulId).append(html_ul);
	
	var content = '';
	if(options.content){
		content=typeof(options.content)=='string'?options.content:'content is no a string';
	}else if(options.url){
		if(typeof(options.url)=='string'){
			//使用iframe
			////固定TAB中IFRAME高度
			var mainHeight = $(document).height() - topHeight;
			content = '<iframe src="'+options.url+'" width="100%" style="margin-top:-25px;" height="'+mainHeight+'" frameborder="no" border="0" marginwidth="0" marginheight="0" scrolling="yes" allowtransparency="yes"></iframe>';
		}else{
			content = 'url is no a string';
		}
	}else{
		content = 'content or url must exist one at least';
	}
	
	//添加到div中
	var html_div = '<div id="tab_content_'+options.name+'" class="tab-pane fade">'+content+'</div>';
	
	
	$('#'+divId).append(html_div);
	
	//如果存在回调函数，则直接调用
	if(typeof(options.callback)=='function'){
		options.callback();
	}
	
	var addActive = typeof(options.active)=='boolean'?options.active:true;
	if(addActive){
		$("#tab_a_"+options.name).click();
	}
	
};

