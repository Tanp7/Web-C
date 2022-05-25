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


//删除
var del = function(id,name){
	swal({
		title:'确实要从最新推荐中移除吗？',
		text:'商品：'+name,
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/newarrival/delete.do',{id:id},function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			swal({
					title:'删除成功',
					icon:'success',
					buttons:'确定'
			}).then(function(value){
				//保存成功，刷新一下记录，重新提交表单
				$('#form_search').get(0).submit();
			});
		});
	});
};

//打开设置排序号的窗口
var setseqno = function(id,seqno,tabloc,code,name){
	$('#label_seqno').text('编号：'+code+' , 名称：'+name);
	jqu.formItem('id','form1').val(id);
	jqu.formItem('seqno','form1').val(seqno);
	jqu.formItem('tabloc','form1').val(tabloc);
	$('#modal_seqno').modal('show');
};

//保存排序号的跳转
var save_seqno = function(){
	var data = jqu.formData('form1');
	
	//排序号必须是数值
	if(data.seqno=='' || isNaN(data.seqno)){
		swal('排序号不正确','','error').then(function(value){
			jqu.formItem('seqno','form1').focus();
		});
		return;
	}
	
	swal({
		title:'确实要调整排序号吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/newarrival/setseqno.do',data,function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			swal({
					title:'排序号调整成功',
					icon:'success',
					buttons:'确定'
			}).then(function(value){
				//保存成功，刷新一下记录，重新提交表单
				$('#form_search').get(0).submit();
			});
		});
	});
};


$(function(){
	
});