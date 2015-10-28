$(function(){
	$('.datatime').datetimepicker({
	    lang:'ch',
		timepicker:false,
		format:'Y-m-d',
		scrollInput:false,
		validateOnBlur:false
	});	
	
	$("#js_save").click(function(){
		$(this).closest("#js_member").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");		
		
		if(!checkFiled())
	        return false;
		var _xsrf = $('input[name="_xsrf"]').val();
		var _mobile = $("#m-mobile").val();
		var _name = $("#m-name").val();
		var _pwd = $("#m-pwd").val();
		var _pwd1 = $("#m-pwd1").val();
		var _email = $("#m-email").val();
		var _weixin = $("#m-weixin").val();
		var _weibo = $("#m-weibo").val();
		var _qq = $("#m-qq").val();
		var _birthday = $("#m-birthday").val();
	
		var _id = $(this).parent().parent().children("#member_id").val();
		$.ajax({
			type:"post",
			url:"/merchant/resetinfo/",
			data: {
				_xsrf:_xsrf,
				//Fuser_mobi: _mobile,
				//Fuser_name: _name,
				Femail: _email,
				Fweixin: _weixin,
				Fweibo: _weibo,
	            Fqq: _qq,
				Fuser_pwd: _pwd,
			},
			success: function(data){
				if(data.stat == "ok"){
	                show_dialog_reload("个人信息","保存成功！");
					//window.location.href = "/merchant/resetinfo/";
				}else{
					//alert(data.msg);
					show_dialog_reload("个人信息",data.msg);
				}
			},
	
			error: function(){
			}
		});
	})
	
	$("#js_cancel").click(function(){
		window.location.href = "/merchant/resetinfo/";
	})
	
	$(".input-txt").keyup(function(){
		$(this).closest("#js_member").find(".error").html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	
	$(".input-txt").blur(function(){
		$(this).closest("#js_member").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});	
})


function checkFiled(e){
//	if($("#m-name").val() == ""){
//		$("#m-name").focus().css("border","1px solid #f00");
//		$(".name-error").html("姓名不能为空");
//		return false;
//	}
	if($("#m-mobile").val() == ""){
		$("#m-mobile").focus().css("border","1px solid #f00");
		$(".mobile-error").html("请填写您的联系电话!");
		return false;
	}

	var _pwd = $("#m-pwd").val();
	var _pwd1 = $("#m-pwd1").val();
    if (_pwd1 != _pwd){
		$("#m-pwd1").focus().css("border","1px solid #f00");
		$(".pwd1-error").html("两次输入密码不一致");
        return false;
    }
    return true;

};

$(".change_passwd").click(function(){
    if ($(this).html() == "重 置"){
        $(this).html("取 消");
        $("#show-pwd").css("display","block");
    }
    else{
        $(this).html("重 置");
        $("#show-pwd").css("display","none");
        $("#m-pwd").val("");
        $("#m-pwd1").val("");
    }
});

