/**
* 将tab的相关应用进行封装
*/
(function(){
	$.icekingTab = function(tabdivstr){
		
		/**
		==================================================================
		私有属性变量的定义
		==================================================================
		*/
		
		//该tab所在的div，容器类
		var tab = null;
		//ttile UL部分
		var tabTitleUl = null;
		//内容部分div
		var tabContentDiv = null;
		
		//当前选中的tabId
		var curActiveTabId='';
		
		//保存设置进来的obj的数据，根据tab的id进行查找的
		//如果已经关闭的，数据还是保留的
		//var curTabsDataArray = new Array();
		
		/**
		已经存在的tab数据保存到对象，
		key=tabId
		value=tab data object
		
		close的时候通过 delete 来删除这个键
		*/
		var curExistTabsData = {};
		
		/**
		==================================================================
		内部方法定义
		==================================================================
		*/
		
		/**
		tab页的初始化
		*/
		var init = function(){
			//tabdivstr 必须是字符串
			if(typeof(tabdivstr)!='string'){
				alert('Parameter tabdivstr must string.');
				return;
			}
			tab = $(tabdivstr);
			if(tab.length!=1){
				alert('Tab selector must one element.');
				return;
			}
			
			//判断parent是否是body
			var isBody = false;
			if(tab.get(0).tagName=='BODY' || tab.get(0).tagName=='body')
				isBody = true;
			
			//如果不是body，则清空parent原来的元素
			if(!isBody){
				tab.empty();
			}
			
			//获得tab的widht和height
			var tabHeight = isBody?$(document).height():tab.height();
			tabHeight = parseInt(tabHeight);
			
			//添加title ul 和 content div
			var tmp = '<ul class="nav nav-tabs"><li><a href="javascript:void(0)">';
			tmp+='All&nbsp;<span class="glyphicon glyphicon-remove">';
			tmp+='</a></li><ul>';
			tab.append(tmp);
			tab.append('<div class="tab-content" style="margin-top:1px;"></div>');
			
			//将着两者保存为jquery对象
			tabTitleUl = tab.children('ul');
			tabContentDiv = tab.children('div');
			
			//第一个li是不允许删除的，关闭所有的tab页面，添加点击事件
			tabTitleUl.children('li:first').click(function(){
				pri_CloseAllTabs();
			});
			
			var titleUlHeight = parseInt(tabTitleUl.height());
			//alert(tabHeight+' , '+titleUlHeight);
			
			//设置内容区域的高度，填充剩余部分
			tabContentDiv.height(tabHeight-titleUlHeight-1);
			
		};
		init();
		
		/**
		关闭所有的tab
		*/
		var pri_CloseAllTabs = function(){
			if(!confirm('Are you sure to close all tabs?'))
				return;
			//标签页中，除了第一个li，其它都要关闭掉
			while(true){
				var tmp_last_li = tabTitleUl.children('li:last');
				if(tmp_last_li.length==0)
					break;
				if(typeof(tmp_last_li.attr('id'))=='undefined')
					break;
				tmp_last_li.remove();
			}
			
			//内容的所有div都要清除
			tabContentDiv.empty();
			
			//当前tab数据清空
			curExistTabsData={};
			
			//当前的tabId恢复空
			curActiveTabId='';
		};
		
		/**
			添加tab内容,json格式数组：
			[
				{
					id:'tab1', //每个tab页的id，前面会自动加入 icetab_tabid
					title:'标题', //面板中显示的文字
					closable:false, //是否允许关闭，默认允许
					html:'', //直接以html形式作为tab页内容
					url:'',  //以iframe外部连接形式，和html二选一，html优先
					onShow:function(){},
					onClose:function(){}  //必须是closable=true时候有效，如果return false 则不关闭
				}
			]
		*/
		var pri_addTabs = function(tabsJson){
			if(tabsJson==null || tabsJson.length==0)
				return;
			//添加完毕之后，将要选择的tabId
			var willSelectTabId='';
			//是否确实有新增加的tab，如果有，则后续要重置tab的onselect 事件
			var hasNewTab=false;
			var tabContentDivHeight = tabContentDiv.height();
			for(var i=0;i<tabsJson.length;i++){
				var obj = tabsJson[i];
				
				//必须包含id
				if(!('id' in obj))
					continue;
				/*if(!('title' in obj))
					continue;*/
				var tmp_id = obj.id;
				
				//判断这个id是否已经在数据中存在了，如果存在，则不需要添加了
				if(tmp_id in curExistTabsData){
					willSelectTabId=tmp_id;
					continue;
				}
				
				//需要新增，将数据保存进去
				curExistTabsData[tmp_id]=obj;
				willSelectTabId=tmp_id;
				hasNewTab=true;
				
				
				var tmp_title = ('title' in obj)?obj.title:'No Title';
				var tmp_closable=('closable' in obj)?obj.closable:true;
				//html和url二选一
				var tmp_html=('html' in obj)?obj.html:'';
				var tmp_url=('url' in obj)?obj.url:'';
				if(tmp_html=='' && tmp_url==''){
					tmp_html='&nbsp;No content.';
				}
				
				//根据json组装html，放入到title和content部分去
				var html_1 = '<li id="icetab_li_'+tmp_id+'"><a id="icetab_li_a_'+tmp_id+'" href="#icetab_cnt_'+tmp_id+'" data-toggle="tab">';
				html_1+=tmp_title;
				if(tmp_closable){
					html_1+='&nbsp;<span class="glyphicon glyphicon-remove">';
				}
				html_1+='</a></li>';
				
				var html_2='<div id="icetab_cnt_'+tmp_id+'" class="tab-pane fade">';
				if(tmp_html!=''){
					html_2+=tmp_html;
				}else if(tmp_url!=''){
					html_2+='<iframe id="icetab_cnt_iframe_'+tmp_id+'" name="iframe_'+tmp_id+'" src="'+tmp_url+'" width="100%" height="'+tabContentDivHeight+'" scrolling="auto"></iframe>';
				}
				html_2+='</div>';
				
				//添加到网页中
				tabTitleUl.append(html_1);
				tabContentDiv.append(html_2);
				//如果是closable=true，需要添加点击事件
				if(tmp_closable){
					$('#icetab_li_'+tmp_id+' span').click(function(){
						//alert($(this).parent().prop('outerHTML'));
						//获取父元素 a 的id，再截取，icetab_li_a_tab2
						var spanclick_curTabId = $(this).parent().attr('id').substring(12);
						var spanclick_onClose = null;
						//数据中存在
						if(spanclick_curTabId in curExistTabsData){
							var curTabDataObj = curExistTabsData[spanclick_curTabId];
							if(('onClose' in curTabDataObj) && typeof(curTabDataObj.onClose)=='function')
								spanclick_onClose=curTabDataObj.onClose;
						}
						pri_closeByTabId(spanclick_curTabId,spanclick_onClose);
					});
				}
				
			}
			
			//如果有新的tab进入，则需要给各个tab重置shown.bs.tab事件
			if(hasNewTab){
				//添加完毕后，整体show事件
				$('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
					// 获取已激活的标签页的名称
					var ashow_activeTabId = $(e.target).attr('id').substring(12);
					curActiveTabId=ashow_activeTabId;
					if(ashow_activeTabId in curExistTabsData){
						var curTabDataObj2 = curExistTabsData[ashow_activeTabId];
						if('onShow' in curTabDataObj2 && typeof(curTabDataObj2.onShow)=='function'){
							curTabDataObj2.onShow();
						}
					}
				});
			}
			
			//选择显示某个id
			pri_selectByTabId(willSelectTabId);
		};
		
		/** 
		根据tabId来删除某个tab页
		*/
		var pri_closeByTabId = function(tabId,onClose){
			//关闭之前，首先调用自定义的onClose方法
			if(onClose!=null){
				var tmp_close_return = onClose();
				//如果有返回值，并且为false，则不关闭
				if(typeof(tmp_close_return)=='boolean' && !tmp_close_return)
					return;
			}
			//alert('删除tab页：'+tabId+' . onClose='+(onClose!=null));
			//移除content的div
			$('#icetab_cnt_'+tabId).remove();
			//移除tab标签的li
			$('#icetab_li_'+tabId).remove();
			
			//移除该tab的数据
			delete(curExistTabsData[tabId]);
			
			//选择最后一个
			pri_selectLastTab();
		};
		
		/** 
		根据tabId来选择某个tab页
		*/
		var pri_selectByTabId = function(tabId){
			$('#icetab_li_a_'+tabId).tab('show');
		};
		
		/** 
		选择最后一个tab，并show
		*/
		var pri_selectLastTab = function(){
			var lilast = tabTitleUl.children('li:last');
			if(lilast.length==0)
				return;
			var lilast_id = lilast.attr('id');
			if(typeof(lilast_id)=='undefined')
				return;
			//最后一页进行选择
			pri_selectByTabId(lilast_id.substring(10));
		};
		
		/**
		==================================================================
		外部方法定义
		==================================================================
		*/
		
		
		/**
		添加tab，可以是数组
		*/
		this.addTab = function(tab){
			if(typeof(tab)=='undefined' || tab==null)
				return;
			if($.isArray(tab)){
				pri_addTabs(tab);
			}else{
				pri_addTabs([tab]);
			}
		};
		
		/**
		添加tab，简洁写法
		*/
		this.add = function(tab){
			if(typeof(tab)=='undefined' || tab==null)
				return;
			if($.isArray(tab)){
				pri_addTabs(tab);
			}else{
				pri_addTabs([tab]);
			}
		};
		
		/**
		返回当前的tabId
		*/
		this.getActiveTabId=function(){
			return curActiveTabId;
		};
		
		/**
		返回当前的iframe对象
		*/
		this.getActiveIframe = function(){
			if(curActiveTabId=='')
				return null;
			var tmp_iframe=$('#icetab_cnt_iframe_'+curActiveTabId);
			if(tmp_iframe.length==0)
				return null;
			return tmp_iframe.get(0).contentWindow;
		};
		
		return this;
	};
})(jQuery);