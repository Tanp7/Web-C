var init = function(){
	alert('hii');
	$('#modal1').modal('hide');
};
//onLoad 椤甸潰鍔犺浇瀹屾瘯鍚庢墽琛?
$(init);

var search = function(){
	jqu.formItem('page', 'form_search').val(1);
	$('#form_search').get(0).submit();
}

var changePage = function(page){
	var curpage = jqu.formItem('page', 'form_search');
	if(curpage==page){
		return;
	}
	jqu.formItem('page', 'form_search').val(page);
	$('#form_search').get(0).submit();
}

// 鍒犻櫎
var remove = function(id){
	if(!confirm('sure?'))
		return;
	
	jqu.loadJson('/remove',{id:id},function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		alert('succeed!');
		$('#form_search').get(0).submit();
	});
};

//打开新增对话框
var presave = function(id){
	
	jqu.loadJson('/presave',{id:id},function(result){
		// 将获得的内容填写到修改表单中
		jqu.formLoad('form_am',result.record);
		//打开对话框
		$('#modal1').modal('show');
	});
};

//提交，保存
var save = function(){
	var data = jqu.formData('form_am');
	// alert(jqu.obj2json(data));
	// 进行必填项的判断
	if(data.code==''){
		alert('need code');
		return;
	}
	if(data.name==''){
		alert('need name');
		return;
	}
	if(data.age==''){
		alert('need age');
		return;
	}
	if(data.salary==''){
		alert('need salary');
		return;
	}
	
	// 保存前的提示
	if(!confirm('sure?'))
		return;
	
	//提交数据进行保存
	jqu.loadJson('/save',data,function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		//保存成功，刷新页面
		alert('succeed');
		$('#form_search').get(0).submit();
	});
	
};