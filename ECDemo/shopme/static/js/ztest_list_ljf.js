var init = function(){
	alert('hii');
	$('#modal1').modal('hide');
};
//onLoad 页面加载完毕后执�?
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

// 删除
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

//�������Ի���
var presave = function(id){
	
	jqu.loadJson('/presave',{id:id},function(result){
		// ����õ�������д���޸ı���
		jqu.formLoad('form_am',result.record);
		//�򿪶Ի���
		$('#modal1').modal('show');
	});
};

//�ύ������
var save = function(){
	var data = jqu.formData('form_am');
	// alert(jqu.obj2json(data));
	// ���б�������ж�
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
	
	// ����ǰ����ʾ
	if(!confirm('sure?'))
		return;
	
	//�ύ���ݽ��б���
	jqu.loadJson('/save',data,function(result){
		if(!result.succ){
			alert(result.stmt);
			return;
		}
		
		//����ɹ���ˢ��ҳ��
		alert('succeed');
		$('#form_search').get(0).submit();
	});
	
};