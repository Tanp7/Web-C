var init = function(){
	alert('init when html is loaded');
};
//onLoad 页面加载完毕后执�?
$(init);

var search = function(){
	alert('search');
	$('#form_search').get(0).submit();
}

//�������Ի���



//-------------
//----zzh------
//-------------

var remove = function(id) {
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
}

//-------------
//----zzh------
//-------------


var presave = function(id){
	
	jqu.loadJson('/presave',{id:id},function(result){
		// ����õ�������д���޸ı�����
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