
//获取验证码
var getCheckCode = function(){
	jqutils.loadJson('/admin/gnrcheckcode.do',function(data){
		$('#check_code').text(data.check_code);
	});
};

//登入操作
var loginAction = function(){
	var fi_sp1 = jqutils.formItem('sp1','ff');
	//表单验证
	var fi_username = jqutils.formItem('username','ff');
	if(fi_username.val()==''){
		fi_sp1.html('请输入用户名');
		fi_username.focus();
		return;
	}
	var fi_password = jqutils.formItem('password','ff');
	if(fi_password.val()==''){
		fi_sp1.html('请输入密码');
		fi_password.focus();
		return;
	}
	var fi_checkcode = jqutils.formItem('checkcode','ff');
	if(fi_checkcode.val()==''){
		fi_sp1.html('请输入验证码');
		fi_checkcode.focus();
		return;
	}
	
	//执行提交动作
	jqutils.loadJson('/admin/login.do',{
		username:fi_username.val(),
		password:fi_password.val(),
		checkcode:fi_checkcode.val()
	},function(data){
		if(!data.succ){
			fi_sp1.html(data.stmt);
			//失败，就切换验证码
			getCheckCode();
			return;
		}
		fi_sp1.html('登入成功，请稍后...');
		setTimeout(function(){
			location.href="/admin/";
		},1000);
	});
	
};

$(function(){
	
	//绑定按钮点击和输入框的回车
	jqu.formItem('btn_login','ff').click(function(){
		loginAction();
	});
	var fi_username = jqutils.formItem('username','ff');
	var fi_password = jqutils.formItem('password','ff');
	var fi_checkcode = jqutils.formItem('checkcode','ff');
	fi_username.keypress(function(e){
		if(e.keyCode==13){
			fi_password.focus();
		}
	});
	fi_password.keypress(function(e){
		if(e.keyCode==13){
			fi_checkcode.focus();
		}
	});
	fi_checkcode.keypress(function(e){
		if(e.keyCode==13){
			loginAction();
		}
	});
	
	
	//点击切换验证码
	$('#check_code').click(function(){
		getCheckCode();
	});
	
	getCheckCode();
	
	fi_username.focus();
	
	//轮播控制
	$('#myCarousel').carousel({
		interval:3000
	});
	
});