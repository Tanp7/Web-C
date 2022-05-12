var init = function(){
	alert('hii');
};
//onLoad ҳ�������Ϻ�ִ��
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