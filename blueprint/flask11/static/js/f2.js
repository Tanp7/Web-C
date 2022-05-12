
var test1 = function(){
	// text 方法，操作元素内部的文本
	// $('p').text('新的文本');
	
	var t = $('#p1').text();
	alert(t);
};

var test2 = function(){
	$('#p1').html('新的文本<i class="fa fa-camera-retro"></i>');
	
	var t = $('#p1').text();
	alert(t);
};

//修改图片显示
var change = function(imgurl){
	$('#img1').attr('src',imgurl);
};

//页面的初始化函数
var init = function(){
	// alert('测试网页初始化');
};


//onLoad 页面加载完毕后执行
$(init);