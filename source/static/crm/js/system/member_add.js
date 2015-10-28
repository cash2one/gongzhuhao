$(function(){
	$("#js_save").click(function(){
		if(!checkFiled())
	        return false;
		var _xsrf = $('input[name="_xsrf"]').val();
		var _name = $("#m-name").val();
		//var _nickname = $("#m-nickname").val();
		var _pwd = $("#m-pwd").val();
		var _pwd1 = $("#m-pwd1").val();
		var _email = $("#m-email").val();
		var _mobile = $("#m-mobile").val();
	    var _permission = $("[name=checkbox]:checked").map(function(){
	                        return $(this).val();
	                    }).get().join(',')
	    $.ajax({
	            type:"post",
	            url: "/merchant/edit/addrole/",
	            data: {
	                _xsrf:_xsrf,
	                user_name: _name,
	                //nick_name: _nickname,
	                user_pwd: _pwd,
	                user_email: _email,
	                user_mobi: _mobile,
	                permission: _permission
	            },
	            success: function(data){
	                var obj = $.parseJSON(data);
	                if(obj.stat == "ok"){
						$("#js_save").attr('disable','disable');
						$("#js_save").addClass("notAllow");
	                    show_dialog_location_href("用户管理","添加成功！",'/merchant/edit/listrole/')
	                    //window.location.href ="/merchant/edit/listrole/";
	                }else{
	                    show_dialog_none_reload("用户管理",obj.msg);
	                }
	            },
	            error: function(){
	            }
		});
	});
	
	$("#js_cancel").click(function(){
		window.location.href = "/merchant/edit/listrole/"
	})
	
	$(".input-txt").keyup(function(){
		$(this).closest("#js_member").find(".error").html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	$(".input-txt").blur(function(){
		$(this).closest("#js_member").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
	$("#js_save").click(function(){
		$(this).closest("#js_member").find(".error").html("");
	   $(this).css("border","1px solid #d8d8d8");	
	});

	$("#checkAll").click(function(){
	    $("input[name='checkbox']").prop("checked", this.checked);
	});
	$("input[name='checkbox']").click(function() {
	    var $subs = $("input[name='checkbox']");
	    $("#checkAll").prop("checked" , $subs.length == $subs.filter(":checked").length ? true :false);
	});
	var $subs = $("input[name='checkbox']");
	$("#checkAll").prop("checked" , $subs.length == $subs.filter(":checked").length ? true :false);
})
function checkFiled(e){
	if($("#m-mobile").val() == ""){
		$("#m-mobile").focus().css("border","1px solid #f00");
		$(".mobile-error").html("手机号码不能为空");
		e.preventDefault();
		return false;
	}
	if(!$("#m-mobile").val().match(/^(((1[0-9][0-9]{1})|159|153)+\d{8})$/)){
		$("#m-mobile").focus().css("border","1px solid #f00");
		$(".mobile-error").html("手机号码格式不正确");
		e.preventDefault();
		return false;
	}
	
	if($("#m-name").val() == ""){
		$("#m-name").focus().css("border","1px solid #f00");
		$(".name-error").html("用户名不能为空");
		e.preventDefault();
		return false;
	}	
	if($("#m-pwd").val() == ""){
		$("#m-pwd").focus().css("border","1px solid #f00");
		$(".pwd-error").html("请输入密码");
		e.preventDefault();
		return false;
	}	
	
	if($("#m-pwd1").val() == ""){
		$("#m-pwd1").focus().css("border","1px solid #f00");
		$(".pwd1-error").html("请输入密码");
		e.preventDefault();
		return false;
	}	
	if($("#m-pwd").val() != $("#m-pwd1").val()){
		$("#m-pwd1").focus().css("border","1px solid #f00");
		$(".pwd1-error").html("两次密码不一致！");
		e.preventDefault();
		return false;
	}	
	if($("#m-mobile").val() == ""){
		$("#m-mobile").focus().css("border","1px solid #f00");
		$(".mobile-error").html("请填写您的联系电话!");
		e.preventDefault();
		return false;
	}	
    return true;
}
