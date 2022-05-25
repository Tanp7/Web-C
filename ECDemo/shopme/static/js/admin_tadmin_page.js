
//查询，恢复页码到1，并提交表单
var search = function(){
	jqu.formItem('page','form_search').val(1);
	$('#form_search').get(0).submit();
};

var presave = function(id){
	jqu.loadJson('/admin/tadmin_presave.do',{id:id},function(result){
		if(!result.succ){
			swal({
				title:result.stmt,
				icon:'error',
				buttons:'确定'
			});
			return;
		}
		//设置到表单项中
		if(id==0){
			$('#rd_type_1').iCheck('check');
		}else{
			$('#rd_type_'+result.record.type).iCheck('check');
		}
		
		jqu.formItem('code','form1').val(result.record.code);
		jqu.formItem('name','form1').val(result.record.name);
		jqu.formItem('username','form1').val(result.record.username);
		jqu.formItem('id','form1').val(result.record.id);
		
		$('#modal_am').modal('show');
	});
};

var save = function(){
	var data = jqu.formData('form1');
	// alert(jqu.obj2json(data));
	
	if(data.code==''){
		jqu.formItem('code','form1').focus();
		return;
	}
	if(data.name==''){
		jqu.formItem('name','form1').focus();
		return;
	}
	if(data.username==''){
		jqu.formItem('username','form1').focus();
		return;
	}
	
	swal({
		title:'确实要保存吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/admin/tadmin_save.do',data,function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			//保存成功，刷新一下记录，重新提交表单
			$('#form_search').get(0).submit();
		});
	});
	
};

//删除
var del = function(id){
	swal({
		title:'确实要删除吗？',
		icon:'info',
		closeOnClickOutside:true,
		closeOnEsc:true,
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/admin/tadmin_del.do',{id:id},function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			//保存成功，刷新一下记录，重新提交表单
			$('#form_search').get(0).submit();
		});
	});
};

//重置密码
var resetpwd = function(id){
	swal({
		title:'确实要重新设置该用户的密码吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/admin/tadmin_resetpwd.do',{id:id},function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			//保存成功，刷新一下记录，重新提交表单
			swal({
				title:'密码重置成功！',
				text:'重置后的密码为：123456',
				icon:'success',
				buttons:'确定'
			});
		});
	});
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

$(function(){
	
	//icheck 的初始化
	$('.my-icheck').iCheck({
		checkboxClass: 'icheckbox_square-green',
		radioClass: 'iradio_square-green'
	});
});