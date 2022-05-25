var init = function(){
	alert('hii');
};

//onLoad 页面加载完毕后执行
$(init);

var test1 = function(){
	$('p').text('111');
	$('#p1').text('mbg');
	//var t = $('#p1').text();
	//alert(t);
};

var test2 = function(){
	$('#p2').html('p2<i class="fa fa-camera-retro"></i>')
	
};

var change = function(imgurl){
	$('#img1').attr('src',imgurl)
};

