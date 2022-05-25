//2018-1-16
//针对jquery的一些常用功能汇总
(function(){
	$.iceking_utils_jquery=function(){
		/**
		==================================================================
		私有属性变量的定义
		
		V1.1: 2018-4-25
			loadJs方法使用jquery.getScript 替代，可以做到异步加载
			loadHtml、loadJson也根据是否有callback的参数，来确定同步还是异步
			
		V1.2: 2019-9-28
			ajax的超时设置为变量，不是固定5000
			增加通过js来判断文件的扩展名和大小的 isFileValid()
		==================================================================
		*/
		var pri_version = 'V1.2';
		var pri_version_date = '2019-09-28';
		var pri_ajax_timeout = 180000;
		
		//记录已经通过loadJs方法装载过的js的url
		var loadedJsArray = new Array();
		
		//默认的文件上传的大小限制和格式限制
		var pri_file_max_size = 1024*1024*5;
		var pri_file_allow_format = ['jpg','jpeg','png','bmp'];
		
		
		/**
		==================================================================
		内部方法定义
		==================================================================
		*/
		
		//表单相关的操作
		var pri_getFormObj = function(formId){
			var jqform=null;
			if(formId.indexOf('#')==0){
				jqform=$(formId);
			}else{
				jqform=$('#'+formId);
			}
			if(jqform.length==0)
				return null;
			return jqform;
		};
		
		//通过jquery，从form中获得表单的字符形式，序列化之后的
		var pri_formDataStr = function(formId){
			var jqform= pri_getFormObj(formId);
			return jqform!=null?jqform.serialize():'';
		};
		
		//获得表单form的Object对象，便于转json字符的
		var pri_formDataObj = function(formId){
			var jqform= pri_getFormObj(formId);
			var obj = new Object();
			if(jqform==null)
				return obj;
			var array = jqform.serializeArray();
			if(array == null || array.length == 0)
				return obj;
			for(var i=0;i<array.length;i++){
				obj[array[i].name]=array[i].value;
			}
			return obj;
		};
		
		//获得表单对象的json字符形式
		var pri_formDataJson = function(formId){
			var jsobj = pri_formDataObj(formId);
			return JSON.stringify(jsobj);
		};
		
		//获得表单中的一个name
		var pri_formItem = function(name,formId){
			var selstr = '[name="'+name+'"]';
			if(typeof(formId)!='undefined' && formId!=null && formId!=''){
				if(formId.indexOf('#') == 0){
					selstr = formId+' '+selstr;
				}else{
					selstr = '#'+formId+' '+selstr;
				}
			}
			var jqobj = $(selstr);
			if(jqobj.length==0){
				return null;
			}
			return jqobj;
		};
		
		//获得表单值，根据name属性
		var pri_formItemVal = function(name,formId){
			var jqobj = pri_formItem(name,formId);
			if(jqobj == null)
				return '';
			return jqobj.val();
		};
		
		//获得表单值，int型，根据name属性
		var pri_formItemInt = function(name,formId){
			var tmpval = pri_formItemVal(name,formId);
			if(tmpval == '')
				return 0;
			return parseInt(tmpval);
		};
		
		//将一个对象中的数据放入到表单相应位置去
		var pri_formLoad = function(formId,obj){
			for(var p in obj){
				var pv = obj[p];
				if(typeof(pv) == 'function')
					continue;
				//根据p去查询form中的一个对象
				var item = pri_formItem(p,formId);
				if(item==null)
					continue;
				item.val(pv);
			}
		};
		
		//直接一个js的object变成json的字符形式
		var pri_objToJson = function(jsobj){
			if(typeof(jsobj)!='object' || jsobj == null)
				return '';
			return JSON.stringify(jsobj);
		};
		
		//将一个json格式的字符串转成js object对象
		var pri_jsonToObj = function(json){
			return eval('(' + json + ')');
		};
		
		//判断某个jquery对象，是否有属性
		var pri_hasAttr = function(jqobjorselector,attr){
			var toftmp = typeof(jqobjorselector);
			
			if(toftmp=='undefined')
				return false;
			
			var jqobj=null;
			
			//如果是jquery对象，则直接使用
			if(toftmp=='object'){
				jqobj=jqobjorselector;
			}else if(toftmp=='string'){
				jqobj=$(toftmp);
			}else{
				return false;
			}
			
			if(jqobj.length==0)
				return false;
			
			if(typeof(attr)=='undefined' || attr==null || attr=='')
				return false;
			
			if(typeof(jqobj.attr(attr))=='undefined')
				return false;
			return true;
		};
		
		//判断内容是否在数组中
		var pri_inArray = function(val,array){
			if(!$.isArray(array))
				return false;
			if(array.length==0)
				return false;
			for(var i=0;i<array.length;i++){
				if(array[i]==val)
					return true;
			}
			return false;
		};
		
		//根据url获取外部的html或者jsp
		var pri_loadHtml = function(url,data,callback){
			var arg_url = arguments[0];
			
			//此处有两种情况，argLen=2，3
			var arg_data;
			var arg_callback;
			if(typeof(arguments[1])=='object'){
				arg_data = arguments[1];
			}else if(typeof(arguments[1])=='function'){
				arg_callback = arguments[1];
			}
			
			if(typeof(arguments[2])=='object'){
				arg_data = arguments[2];
			}else if(typeof(arguments[2])=='function'){
				arg_callback = arguments[2];
			}
			//根据callback区分同步还是异步
			var isasync = (typeof(arg_callback)=='function');
			//第一个url参数必须是字符型
			if(typeof(arg_url)!='string'){
				if(isasync)
					return;
				else
					return '';
			}
			
			var fetch_result_html = null;
			var tmpdata = null;
			var tmpmethod = 'GET';
			if(typeof(arg_data)=='object'){
				tmpdata = arg_data;
				tmpmethod = 'POST';
			}
			
			//如果callback为函数，则使用异步方式
			if(isasync){
				$.ajax({
					async:true,
					timeout:pri_ajax_timeout,
					dataType:'HTML',
					type:tmpmethod,
					url:arg_url,
					data:tmpdata,
					cache:false,
					success:function(result,status,xhr){
						fetch_result_html = result;
						arg_callback(fetch_result_html);
					}
				});
				return;
			}
			
			//如果没有callback，则使用同步方式
			$.ajax({
				async:false,
				timeout:pri_ajax_timeout,
				dataType:'HTML',
				type:tmpmethod,
				url:arg_url,
				data:tmpdata,
				cache:false,
				success:function(result,status,xhr){
					fetch_result_html = result;
				}
			});
			return fetch_result_html;
		};
		
		//请求json格式的返回，可以是post的方式的
		var pri_loadJson = function(url,data,callback){
			var arg_url = arguments[0];
			
			var arg_data;
			var arg_callback;
			if(typeof(arguments[1])=='object'){
				arg_data = arguments[1];
			}else if(typeof(arguments[1])=='function'){
				arg_callback = arguments[1];
			}
			
			if(typeof(arguments[2])=='object'){
				arg_data = arguments[2];
			}else if(typeof(arguments[2])=='function'){
				arg_callback = arguments[2];
			}
			
			//根据callback区分同步还是异步
			var isasync = (typeof(arg_callback)=='function');
			//第一个url参数必须是字符型
			if(typeof(arg_url)!='string'){
				if(isasync)
					return;
				else
					return null;
			}
			
			var json_result = null;
			
			var tmpdata = null;
			var tmpmethod = 'GET';
			if(typeof(arg_data)=='object'){
				tmpdata = arg_data;
				tmpmethod = 'POST';
			}
			
			if(isasync){
				$.ajax({
					async:true,
					timeout:pri_ajax_timeout,
					dataType:'TEXT',
					type:tmpmethod,
					url:arg_url,
					data:tmpdata,
					cache:false,
					success:function(result,status,xhr){
						json_result = eval('(' + result + ')');
						arg_callback(json_result);
					}
				});
				return;
			}
			
			$.ajax({
				async:false,
				timeout:pri_ajax_timeout,
				dataType:'TEXT',
				type:tmpmethod,
				url:arg_url,
				data:tmpdata,
				cache:false,
				success:function(result,status,xhr){
					json_result = eval('(' + result + ')')
				}
			});
			return json_result;
		};
		
		//将数据对象应用到模板html
		// 数据部分使用： ${obj.name}
		var pri_templateHtml_one = function(htmltmpl,obj){
			var tmpl_html=htmltmpl;
			while(true){
				var idx1=tmpl_html.indexOf('${');
				var idx2=tmpl_html.indexOf('}');
				if(idx1==-1 || idx2==-1)
					break;
				//idx1之前的字符串
				var bfstr=tmpl_html.substring(0,idx1);
				//${name}
				var datastr=tmpl_html.substring(idx1+2,idx2);
				//使用eval获取数据
				var datatmp = eval('obj.'+datastr);
				if(typeof(datatmp)=='undefined'){
					datatmp='undefined';
				}
				//idx2之后的字符传
				var aftstr=tmpl_html.substring(idx2+1);
				//重新组装
				tmpl_html=bfstr+datatmp+aftstr;
			}
			return tmpl_html;
		};
		
		//模板的数据可以是数组
		var pri_templateHtml=function(htmltmpl,obj){
			if(typeof(obj)!='object')
				return htmltmpl;
			
			//如果数据是数组，则循环模板
			if(Array.isArray(obj)){
				var tmparrayhtml='';
				for(var i=0;i<obj.length;i++){
					tmparrayhtml+=pri_templateHtml_one(htmltmpl,obj[i]);
				}
				return tmparrayhtml;
			}
			
			return pri_templateHtml_one(htmltmpl,obj);
		};
		
		//同时动态加载html（jsp）模板和json数据
		var pri_loadTmpl = function(htmlUrl,htmlData,jsonUrl,jsonData,callback){
			var arg_htmlUrl;
			var arg_htmlData;
			var arg_jsonUrl;
			var arg_jsonData;
			var arg_callback;
			//循环放置参数
			for(var i=0;i<arguments.length;i++){
				//所有的参数总共就是 string，object，function 三种类型的
				if(typeof(arguments[i])=='string'){
					//url，html模板的url优先
					if(typeof(arg_htmlUrl)=='undefined')
						arg_htmlUrl = arguments[i];
					else if(typeof(arg_jsonUrl)=='undefined')
						arg_jsonUrl = arguments[i];
				}else if(typeof(arguments[i])=='object'){
					//参数，要以json的优先，如果此时还没有jsonurl，则给html用
					if(typeof(arg_jsonUrl)=='undefined'){
						//jsonurl 还没有赋值，那么首选给htmldata用
						if(typeof(arg_htmlData)=='undefined')
							arg_htmlData = arguments[i];
						else if(typeof(arg_jsonData)=='undefined')
							arg_jsonData = arguments[i];
					}else{
						//jsonurl已经赋值了，那么首选的给jsondata用
						if(typeof(arg_jsonData)=='undefined')
							arg_jsonData = arguments[i];
						else if(typeof(arg_htmlData)=='undefined')
							arg_htmlData = arguments[i];
					}
				}else if(typeof(arguments[i])=='function'){
					if(typeof(arg_callback)=='undefined')
						arg_callback = arguments[i];
				}
			}
			
			
			//根据callback区分同步还是异步
			var isasync = (typeof(arg_callback)=='function');
			//两个url必须为string
			if(typeof(arg_htmlUrl)!='string' || typeof(arg_jsonUrl)!='string'){
				if(isasync)
					return;
				else
					return '';
			}
			
			
			if(isasync){
				//异步方式
				
				//采用$.Deferred和$.when方法
				var rst_html_tmpl;
				var rst_json_data;
				
				
				//请求html模板
				var tmpFn1 = function(){
					var dtd = $.Deferred();
					if(typeof(arg_htmlData)=='object'){
						//post方式
						pri_loadHtml(arg_htmlUrl,arg_htmlData,function(result){
							rst_html_tmpl = result;
							dtd.resolve();
						});
					}else{
						//get方式
						pri_loadHtml(arg_htmlUrl,function(result){
							rst_html_tmpl = result;
							dtd.resolve();
						});
					}
					return dtd.promise();
				};
				
				//请求json数据
				var tmpFn2 = function(){
					var dtd = $.Deferred();
					if(typeof(arg_jsonData)=='object'){
						//post方式
						pri_loadJson(arg_jsonUrl,arg_jsonData,function(result){
							rst_json_data = result;
							dtd.resolve();
						});
					}else{
						//get方式
						pri_loadJson(arg_jsonUrl,function(result){
							rst_json_data = result;
							dtd.resolve();
						});
					}
					return dtd.promise();
				};
				
				$.when(tmpFn1(),tmpFn2()).done(function(){
					if(typeof(rst_html_tmpl)=='string' && typeof(rst_json_data)=='object'){
						//将两者组装获得最终的html
						var rst_html = pri_templateHtml(rst_html_tmpl,rst_json_data);
						//执行回掉函数
						arg_callback(rst_html,rst_html_tmpl,rst_json_data);
					}else{
						//错误，执行回掉函数
						arg_callback('Error. can not load result.');
					}
				});
				
				
			}else{
				//同步方式
				
				//请求html模板
				var rst_html_tmpl = pri_loadHtml(arg_htmlUrl,arg_htmlData);
				
				//请求json数据
				var rst_json_data = pri_loadJson(arg_jsonUrl,arg_jsonData);
				
				//将两者组装获得最终的html
				var rst_html = pri_templateHtml(rst_html_tmpl,rst_json_data);
				
				return rst_html;
			}
			
		};
		
		//动态加载js文件，后面加上随机数，不缓存
		//需要使用script标签生成，使用docment.write
		var pri_loadJs_one = function(url,callback){
			//document.write('<script type="text/javascript" src="'+url+'?'+Math.random()+'"></script>');
			
			//判断url是否在已经加载的数组中
			var loaded = pri_inArray(url,loadedJsArray);
			
			//已经加载了
			if(loaded){
				//判断是否调用callback
				if(typeof(callback)=='function')
					callback.call();
				return;
			}
			
			//未加载，则需要加载后调用callback
			$.getScript(url,function(){
				//将url放入到array中
				loadedJsArray[loadedJsArray.length]=url;
				//判断是否调用callback
				if(typeof(callback)=='function')
					callback.call();
			});
			
		};
		
		//使用延时 Deferred 加载js
		var pri_deferJs = function(url){
			var dtd = $.Deferred();
			
			$.getScript(url,function(){
				//console.log(url+' 加载完毕');
				loadedJsArray[loadedJsArray.length]=url;
				dtd.resolve();
			});
			
			return dtd.promise();
		};
		
		//url可以多个，是数组形式
		var pri_loadJs = function(url,callback){
			//只有一个url的js，则调用 pri_loadJs_one
			if(!Array.isArray(url)){
				pri_loadJs_one(url,callback);
				return;
			}
			
			//多个js一起调用，需要在全部调用完毕后，再执行callback
			//找出不在已加载数组中的那些url
			var unloadUrlArray = new Array();
			for(var i=0;i<url.length;i++){
				if(!pri_inArray(url[i],loadedJsArray))
					unloadUrlArray[unloadUrlArray.length]=url[i];
			}
			
			//判断是否已经都加载了
			if(unloadUrlArray.length==0){
				//判断是否需要调用callback
				if(typeof(callback)=='function')
					callback.call();
				return;
			}
			
			//采用$.Deferred()来实现延时
			var deferArray = new Array();
			for(var i=0;i<unloadUrlArray.length;i++){
				deferArray[deferArray.length] = pri_deferJs(unloadUrlArray[i]);
			}
			
			//存在没有加载过的，则加载，使用when
			$.when.apply(deferArray).done(function(){
				//将这些未加载的url，添加到已经加载数组中
				/*for(var i=0;i<unloadUrlArray.length;i++){
					loadedJsArray[loadedJsArray.length]=unloadUrlArray[i];
				}*/
				//判断是否需要调用callback
				//解决不了全部加载问题，所以使用了延时
				if(typeof(callback)=='function'){
					setTimeout(callback,deferArray.length*100);
				}
			});
			
		};
		
		//在js端判断上传的文件是否符合，返回ok表示符合要求
		var pri_isFileValid = function(fileid,maxSize,allowFormat){
			//获得文件框的值和大小
			var file = null;
			if(fileid.indexOf('#')==0){
				file=$(fileid);
			}else{
				file=$('#'+fileid);
			}
			if(file.length==0)
				return 'file id is not exist. '+fileid;
			var file_value = file[0].value.toLowerCase();
			if(file_value=='')
				return 'file not choose.';
			
			var file_size = file[0].files[0].size;
			if(file_size<=0)
				return 'file is empty or error. '+file_size;
			
			alert(file_value+'   '+file_size);
			
			return 'no';
		};
		
		
		/**
		==================================================================
		外部方法定义
		==================================================================
		*/
		
		//返回本工具的版本号
		this.version = function(){
			return pri_version+'('+pri_version_date+')';
		};
		
		//根据表单id号，获得表单属性的js object对象
		this.formData = function(formId){
			return pri_formDataObj(formId);
		};
		
		//根据表单id号，获得表单属性的紧凑型字符参数形式
		this.formDataStr = function(formId){
			return pri_formDataStr(formId);
		};
		
		//根据表单id号，获得表单属性的json字符串形式
		this.formDataJson = function(formId){
			return pri_formDataJson(formId);
		};
		
		//根据表单属性name，获得该属性的jquery对象
		this.formItem = function(name,formId){
			return pri_formItem(name,formId);
		};
		
		//根据表单属性name，获得该属性的字符型值
		this.formVal = function(name,formId){
			return pri_formItemVal(name,formId);
		};
		
		//根据表单属性name，获得该属性的整数型值
		this.formInt = function(name,formId){
			return pri_formItemInt(name,formId);
		};
		
		//将js object 装载到表单属性中
		this.formLoad = function(formId,obj){
			pri_formLoad(formId,obj);
		};
		
		//js object 对象转成 json格式字符串
		this.obj2json = function(obj){
			return pri_objToJson(obj);
		};
		
		//json格式字符串转成js object对象
		this.json2obj = function(json){
			return pri_jsonToObj(json);
		};
		
		//判断jquery对象是否包含某个属性名称
		this.hasAttr = function(jqobjorselector,attr){
			return pri_hasAttr(jqobjorselector,attr);
		};
		
		//判断数组array是否包含val值
		this.inArray = function(val,array){
			return pri_inArray(val,array);
		};
		
		//ajax方式获得html，可以携带动态参数data
		//参数data可以省略，省略则表示get方式，否则表示post方式
		//如果有callback，则使用异步方式调用，否则同步方式调用
		//回调函数callback携带参数：html，表示load之后获得的html字符串
		this.loadHtml = function(url,data,callback){
			return pri_loadHtml(url,data,callback);
		};
		
		//ajax方式获得json，可以携带动态参数data
		//参数data可以省略，省略则表示get方式，否则表示post方式
		//如果有callback，则使用异步方式调用，否则同步方式调用
		//回调函数callback携带参数：data，表示load之后的json object
		this.loadJson = function(url,data,callback){
			return pri_loadJson(url,data,callback);
		};
		
		//加载js文件，带随机数，避免浏览器缓存
		//url可以为数组，则表示多个js同时加载
		//回调函数callback无参数，紧表示js加载成功后的动作
		this.loadJs = function(url,callback){
			return pri_loadJs(url,callback);
		};
		
		//将data数据加载到模板html中，获得新的html
		this.tmpl = function(html,data){
			return pri_templateHtml(html,data);
		};
		
		//同时加载模板和数据
		//参数：htmlData、jsonData和callback可以省略
		//如果有callback，则使用异步方式调用，否则同步方式调用
		//回调函数callback携带参数：
		//  html：表示模板和数据组装完毕后的结果html字符串
		//  tmpl: 表示获取到的模板原始html字符串
		//  data：表示获取到的数据 json object
		this.loadTmpl = function(htmlUrl,htmlData,jsonUrl,jsonData,callback){
			return pri_loadTmpl(htmlUrl,htmlData,jsonUrl,jsonData,callback);
		};
		
		//js判断上传的文件是否符合要求，返回ok表示成功
		this.isFileValid = function(fileid,maxSize,allowFormat){
			return pri_isFileValid(fileid,maxSize,allowFormat);
		};
		
	};
})(jQuery);

//定义变量
var jqutils = new $.iceking_utils_jquery;
var jqu = jqutils;