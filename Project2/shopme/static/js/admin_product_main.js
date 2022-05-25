
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

var presave = function(id){
	jqu.loadJson('/product/presave.do',{id:id},function(result){
		if(!result.succ){
			swal({
				title:result.stmt,
				icon:'error',
				buttons:'确定'
			});
			return;
		}
		//设置到表单项中
		
		//使用 jqu.formLoad 方法可以根据name属性一次性的将数据加载到表单项中
		jqu.formLoad('form1',result.record);
		
		
		// jqu.formItem('id','form1').val(result.record.id);
		
		$('#modal_am').modal('show');
	});
};

var save = function(){
	var data = jqu.formData('form1');
	// alert(jqu.obj2json(data));
	// return;
	
	//判断表单的必填项
	if(data.name==''){
		jqu.formItem('name','form1').focus();
		return;
	}
	if(data.code==''){
		jqu.formItem('code','form1').focus();
		return;
	}
	if(data.title==''){
		jqu.formItem('title','form1').focus();
		return;
	}
	if(data.markshort==''){
		jqu.formItem('markshort','form1').focus();
		return;
	}
	if(data.size==''){
		jqu.formItem('size','form1').focus();
		return;
	}
	if(data.tags==''){
		jqu.formItem('tags','form1').focus();
		return;
	}
	if(data.type1==''){
		jqu.formItem('type1','form1').focus();
		return;
	}
	if(data.type2==''){
		jqu.formItem('type2','form1').focus();
		return;
	}
	//价格和库存必须为数值
	if(data.priceold=='' || isNaN(data.priceold)){
		jqu.formItem('priceold','form1').focus();
		return;
	}
	if(data.pricenew=='' || isNaN(data.pricenew)){
		jqu.formItem('pricenew','form1').focus();
		return;
	}
	if(data.stock=='' || isNaN(data.stock)){
		jqu.formItem('stock','form1').focus();
		return;
	}
	
	swal({
		title:'确实要保存吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/save.do',data,function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			swal({
					title:'保存成功',
					icon:'success',
					buttons:'确定'
			}).then(function(value){
				//保存成功，刷新一下记录，重新提交表单
				$('#form_search').get(0).submit();
			});
			
		});
	});
	
};

//删除
var del = function(id,name){
	swal({
		title:'确实要删除商品“'+name+'”吗？',
		text:'注意: 同时会删除该商品相关的其它数据',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/delete.do',{id:id},function(result){
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




// 给商品添加图片
var addImg = function(id){
	//表单重置
	$('#form2').get(0).reset();
	
	//根据现在有多少个小图片的div，来设置新加入的图片的 seqno
	var div_imgthumb = $('#div_imgthumb_'+id);
	if(div_imgthumb.length>0){
		var count = div_imgthumb.children().length;
		//最多8个
		var seqno = count<8?count+1:8;
		jqu.formItem('seqno','form2').val(seqno);
	}
	
	//将商品id设置进去
	jqu.formItem('proid','form2').val(id);
	
	$('#modal_img').modal('show');
};

//判断图片是否符合要求
var isImgValid = function(name){
	//拿到文件名
	var filename = jqu.formVal(name,'form2');
	if(filename==''){
		return '请首先选择图片';
	}
	//图片的扩展名必须是：jpg、jpeg、png、bmp
	var lidx = filename.lastIndexOf('.');
	if(lidx==-1){
		return '图片格式必须是：jpg、jpeg、png、bmp格式';
	}
	var fileext = filename.substring(lidx+1).toUpperCase();
	if(fileext!='JPG' && fileext!='JPEG' && fileext!='PNG' && fileext!='BMP'){
		return '图片格式必须是：jpg、jpeg、png、bmp格式';
	}
	
	//文件大小判断，必须先获取到文本框对象，next()才表示html中的元素
	var filesize = jqu.formItem(name,'form2').get(0).files[0].size;
	if(name=='imgnormal'){
		//正常图片建议尺寸：360 * 360，大小不超过 500K
		if(filesize>500*1024){
			return '正常图片必须小于 500K';
		}
	}else if(name=='imgthumb'){
		//小图片建议尺寸：80 * 80，大小不超过 100K
		if(filesize>100*1024){
			return '小图片必须小于 100K';
		}
	}else if(name=='imglarge'){
		//大图片建议尺寸：800 * 800，大小不超过 1M
		if(filesize>1024*1024){
			return '大图片必须小于 1M';
		}
	}else{
		return '图片名称不正确';
	}
	
	return 'ok';
};

//保存图片
var saveImg = function(){
	//三个图片都必须填写，且符合要求
	var stmt = isImgValid('imgnormal');
	if(stmt!='ok'){
		swal(stmt,'','error');
		return;
	}
	stmt = isImgValid('imgthumb');
	if(stmt!='ok'){
		swal(stmt,'','error');
		return;
	}
	stmt = isImgValid('imglarge');
	if(stmt!='ok'){
		swal(stmt,'','error');
		return;
	}
	
	swal({
		title:'确实要保存图片吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		// 采用 jquery.form 的ajax方式提交表单
		$('#form2').ajaxSubmit({
			url:'/product/saveimg.do',
			type:'post',
			dataType:'json',
			success:function(result){
				if(!result.succ){
					swal('保存失败',data.error,'error');
					return;
				}
				
				swal({
					title:'保存成功',
					icon:'success',
					buttons:'确定'
				}).then(function(value){
					$('#form_search').get(0).submit();
				});
				
				
	        },
	        error:function(XmlHttpRequest,textStatus,errorThrown){
	        	alert('Error: '+textStatus+', '+errorThrown);
	        }
		});
		
		
	});
};

// 点击商品小图的时候，把正常图片设置到默认图片位置
var setnormalimg = function(imgurl,proid){
	$('#defaultimg_'+proid).attr('src',imgurl);
};

// 点击小图下方的按钮，显示 大图片
var viewlargeimg = function(imgurl){
	$('#img_large').attr('src',imgurl);
	$('#modal_view_large').modal('show');
};

//点击小图片下方的按钮，设置 排序号
var setimgseqno = function(id,seqno,imgnormal){
	// 弹出框 中显示图片正常大小
	$('#img_seqno_normal').attr('src',imgnormal);
	// 设置排序号
	jqu.formItem('seqno','form3').val(seqno);
	// 设置图片 tproimg 表的 id号
	jqu.formItem('id','form3').val(id);
	
	$('#modal_seqno').modal('show');
};

// 修改图片的排序号
var saveimgseqno = function(){
	var data = jqu.formData('form3');
	swal({
		title:'确实要改变图片排序号吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/setimgseqno.do',data,function(result){
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				return;
			}
			swal({
					title:'保存成功',
					icon:'success',
					buttons:'确定'
			}).then(function(value){
				$('#form_search').get(0).submit();
			});
			
		});
		
	});
};

//点击小图下方的按钮，删除商品图片
var deleteimg = function(id){
	swal({
		title:'确实要删除该图片吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/deleteimg.do',{id:id},function(result){
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
				$('#form_search').get(0).submit();
			});
			
		});
		
	});
};

//加入每日特价
var add_to_dayspecial = function(id,imgurl){
	$('#img_dayspecial').attr('src',imgurl);
	jqu.formItem('proid','form4').val(id);
	//排序号默认1
	jqu.formItem('seqno','form4').val(1);
	
	$('#modal_add_dayspecial').modal('show');
};

//保存 每日特价
var save_dayspecial = function(){
	var data = jqu.formData('form4');
	if(data.seqno=='' || isNaN(data.seqno)){
		swal('排序号不正确','','error').then(function(value){
			jqu.formItem('seqno','form4').focus();
		});
		return;
	}
	
	swal({
		title:'确实要加入到“每日特价”吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/add_dayspecial.do',data,function(result){
			$('#modal_add_dayspecial').modal('hide');
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				
				return;
			}
			swal({
					title:'保存成功',
					icon:'success',
					buttons:'确定'
			});			
		});
		
	});
	
};

//加入新品推荐
var add_to_newarrival = function(id,imgurl){
	$('#img_newarrival').attr('src',imgurl);
	jqu.formItem('proid','form5').val(id);
	//排序号默认1
	jqu.formItem('seqno','form5').val(1);
	//默认的tab页位置：空
	jqu.formItem('tabloc','form5').val('');
	
	$('#modal_add_newarrival').modal('show');
};

//保存 新品推荐
var save_newarrival = function(){
	var data = jqu.formData('form5');
	if(data.seqno=='' || isNaN(data.seqno)){
		swal('排序号不正确','','error').then(function(value){
			jqu.formItem('seqno','form5').focus();
		});
		return;
	}
	
	//tab页位置可以空，空的话，默认就是: tab-default
	
	swal({
		title:'确实要加入到“新品推荐”吗？',
		icon:'info',
		buttons:['取消','确定']
	}).then(function(value){
		if(value==null)
			return;
		
		jqu.loadJson('/product/add_newarrival.do',data,function(result){
			$('#modal_add_newarrival').modal('hide');
			if(!result.succ){
				swal({
					title:result.stmt,
					icon:'error',
					buttons:'确定'
				});
				
				return;
			}
			swal({
					title:'保存成功',
					icon:'success',
					buttons:'确定'
			});			
		});
		
	});
};

$(function(){
	
	
});