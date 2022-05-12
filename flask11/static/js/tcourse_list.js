//查询，恢复页码到1，并提交表单
var search = function(){
	jqu.formItem('page','form_search').val(1);
	$('#form_search').get(0).submit();
};

//翻页栏切换
var changePage = function(page){
	//找到当前页
	var curpage = jqu.formInt('page','form_search');
	if(curpage==page){
		//如果将要跳转的页码和当前页码一致，就不需要处理了
		return;
	}
	
	//将表单中隐藏域的页码切换为page，并提交表单
	jqu.formItem('page','form_search').val(page);
	$('#form_search').get(0).submit();
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
		alert('课程编号 必须填写');
		return;
	}
	if(data.name==''){
		alert('课程名称 必须填写');
		return;
	}
	if(data.score==''){
		alert('学分 必须填写');
		return;
	}
	if(data.institute==''){
		alert('开课学院 必须填写');
		return;
	}
	
	// 保存前的提示
	if(!confirm('确实要保存吗？'))
		return;
	
	//提交数据进行保存
	jqu.loadJson('/save',data,function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		//保存成功，刷新页面
		alert('保存成功');
		$('#form_search').get(0).submit();
	});
	
};

// 删除
var remove = function(id){
	if(!confirm('确实要删除该记录吗？'))
		return;
	
	jqu.loadJson('/remove',{id:id},function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		alert('删除成功');
		$('#form_search').get(0).submit();
	});
};
