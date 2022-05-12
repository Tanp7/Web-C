//Bootstrap and jquery utils

//======================================================================
//=====================表单提交相关的数据转换=============================
//======================================================================
//获得表单的jquery对象
var fnGetFormJqObj = function(formId){
	if(formId == null || formId == '')
		return null;
	var jqobj = null;
	if(formId.substr(0,1) == '#'){
		jqobj = $(formId);
	}else{
		jqobj = $('#'+formId);
	}
	if(jqobj == null || jqobj.length==0)
		return null;
	return jqobj;
};

//通过jquery，从form中获得表单的字符形式，序列化之后的
var fnJqFormDataStr = function(formId){
	var jqform = fnGetFormJqObj(formId);
	if(jqform == null)
		return '';
	return jqform.serialize();
};

//获得表单form的Object对象，便于转json字符的
var fnJqFormDataObj = function(formId){
	var jqform = fnGetFormJqObj(formId);
	if(jqform == null)
		return null;
	var array = jqform.serializeArray();
	if(array == null || array.length == 0)
		return null;
	var obj = new Object();
	for(var i=0;i<array.length;i++){
		obj[array[i].name]=array[i].value;
	}
	return obj;
};

//获得表单对象的json字符形式
var fnJqFormDataJson = function(formId){
	var jsobj = fnJqFormDataObj(formId);
	if(jsobj == null)
		return '';
	return JSON.stringify(jsobj);
};

//获得表单中的一个name
var fnJqFormByName = function(namevalue,formId){
	var selstr = '[name="'+namevalue+'"]';
	if(formId!=null && formId!=''){
		if(formId.substr(0,1) == '#'){
			selstr = formId+' '+selstr;
		}else{
			selstr = '#'+formId+' '+selstr;
		}
	}
	var jqobj = $(selstr);
	if(jqobj == null || jqobj.length==0)
		return null;
	return jqobj;
};

//获得表单值，根据name属性
var fnJqFormByNameStr = function(namevalue,formId){
	var jqobj = fnJqFormByName(namevalue,formId);
	if(jqobj == null)
		return '';
	return jqobj.val();
};

//获得表单值，int型，根据name属性
var fnJqFormByNameInt = function(namevalue,formId){
	var jqobj = fnJqFormByName(namevalue,formId);
	if(jqobj == null)
		return 0;
	return parseInt(jqobj.val());
};

//直接一个js的object变成json的字符形式
var fnJsObjectToJsonStr = function(jsobj){
	if(jsobj == null)
		return '';
	return JSON.stringify(jsobj);
};

//从一个html或者jsp中load内容到指定的位置
var fnJqLoadHtml = function(htmlUrl,destId){
	//目标必须存在
	if(destId == null || destId == '')
		return;
	//判断目标id是否有#开头
	var dstId = destId;
	//获得目标的jquery object，不存在的话，直接返回
	var destJqObj = $(dstId);
	if(destJqObj == null || destJqObj.length==0)
		return;
	//目标清空原来的html内容
	destJqObj.empty();
	//通过get方法发送请求
	$.get(htmlUrl+'?rnd='+Math.random(),function(data,status){
		if(status!='success'){
			//错误时候，直接在目标中添加错误信息
			destJqObj.html('Load html from template error. url='+htmlUrl);
			return;
		}
		destJqObj.html(data);
	},'html');
};

//从一个html的模板中装载到页面
var fnJqLoadHtmlFromTmpl = function(htmlUrl,jsonData,destId){
	//目标必须存在
	if(destId == null || destId == '')
		return;
	//判断目标id是否有#开头
	var dstId = destId;
	//获得目标的jquery object，不存在的话，直接返回
	var destJqObj = $(dstId);
	if(destJqObj == null || destJqObj.length==0)
		return;
	//目标清空原来的html内容
	//destJqObj.html('');
	destJqObj.empty();
	//通过get方法发送请求
	$.get(htmlUrl+'?rnd='+Math.random(),function(data,status){
		if(status!='success'){
			//错误时候，直接在目标中添加错误信息
			destJqObj.html('Load html from template error. url='+htmlUrl);
			return;
		}
		//成功的话，生成模板，并添加到指定目标位置，模板的名字就是url名字
		$.template(htmlUrl,data);
		//var tmpltmpl = $.tmpl(htmlUrl,jsonData);
		//alert(tmpltmpl.html());
		$.tmpl(htmlUrl,jsonData).appendTo(dstId);
	},'html');
};

//获取当前脚本的，bootstrap所在的文件夹
var fnJqBootstrapPath = function(){
	return '/weweb/bootstrap-3.3.5-dist/';
};

//初始化弹出消息使用的几个modal窗口
//判断消息是否已经初始化了，根据特定的alert modal的id是否存在来判断
var fnJqMessageInited = function(){
	var msgObj = $('#jqbs_tmpl_modal_alert');
	if(msgObj == null || msgObj.length==0)
		return false;
	return true;
};
//初始化消息对象，一般页面开始时候调用
var fnJqInitMessage = function(){
	if(fnJqMessageInited())
		return;
	//去bootstrap目录下的 tmpl_jqbs_message.html中load内容并append到body中
	var msgtmplurl = fnJqBootstrapPath()+'tmpl_jqbs_message.html';
	$.get(msgtmplurl+'?rnd='+Math.random(),function(data,status){
		if(status!='success'){
			//错误时候，直接在目标中添加错误信息
			alert('Load html from template error. url='+htmlUrl);
			return;
		}
		//成功，将返回的html插入到body中
		$(data).appendTo('body');
	},'html');
};

//弹出提示消息
var fnAlert = function(msg,delay){
	if(!fnJqMessageInited()){
		alert('消息函数未初始化');
		return;
	}
	//图标和文字切换一下
	$('#jqbs_tmpl_modal_alert_icon').attr('src',fnJqBootstrapPath()+'icon128/info_mail.png');
	$('#jqbs_tmpl_modal_alert_words').html(msg);
	
	//yes和no 两个按钮隐藏
	$('#jqbs_tmpl_modal_alert_btn_yes').hide();
	$('#jqbs_tmpl_modal_alert_btn_no').hide();
	
	if(delay!=null && delay>0){
		setTimeout(function(){
			$('#jqbs_tmpl_modal_alert').modal('show');
		},delay);
	}else{
		$('#jqbs_tmpl_modal_alert').modal('show');
	}
};

//弹出确认框，yes和no的操作可以自定义的
var fnConfirm = function(msg,yesCallback,noCallback,autoclose){
	if(!fnJqMessageInited()){
		alert('消息函数未初始化');
		return;
	}
	
	//图标和文字切换
	$('#jqbs_tmpl_modal_alert_icon').attr('src',fnJqBootstrapPath()+'icon128/faq.png');
	$('#jqbs_tmpl_modal_alert_words').html(msg);
	
	//yes和no 两个按钮可见
	$('#jqbs_tmpl_modal_alert_btn_yes').show();
	$('#jqbs_tmpl_modal_alert_btn_no').show();
	
	
	//设置yes和no的callback方法
	$('#jqbs_tmpl_modal_alert_btn_yes').unbind('click');
	$('#jqbs_tmpl_modal_alert_btn_yes').click(function(){
		if(yesCallback!=null && typeof(yesCallback)=='function'){
			yesCallback.call();
		}
		if(autoclose==null || autoclose)
			$('#jqbs_tmpl_modal_alert').modal('hide');
	});
	
	$('#jqbs_tmpl_modal_alert_btn_no').unbind('click');
	$('#jqbs_tmpl_modal_alert_btn_no').click(function(){
		if(noCallback!=null && typeof(noCallback)=='function'){
			noCallback.call();
		}
		if(autoclose==null || autoclose)
			$('#jqbs_tmpl_modal_alert').modal('hide');
	});
	
	$('#jqbs_tmpl_modal_alert').modal('show');
	
};
