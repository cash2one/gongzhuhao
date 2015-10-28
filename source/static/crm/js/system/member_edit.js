$(function(){
	$("#js_save").click(function(){
		if(!checkFiled())
	        return false;
		var _xsrf = $('input[name="_xsrf"]').val();
		var _name = $("#m-name").val();
	//	var _nickname = $("#m-nickname").val();
		var _pwd = $("#m-pwd").val();
		var _pwd1 = $("#m-pwd1").val();
		var _email = $("#m-email").val();
		var _mobile = $("#m-mobile").val();	
	
	    var _permission = $("[name=checkbox]:checked").map(function(){
	                        return $(this).val();
	                    }).get().join(',')
	
		var _id = $(this).parent().parent().children("#member_id").val();
		$.ajax({
	        type:"post",
	        url:"/merchant/edit/editrole/"+_id+"/",
	        data: {
	            _xsrf:_xsrf,
	            user_name: _name,
	//                nick_name: _nickname,
	            user_pwd: _pwd,
	            user_email: _email,
	            user_mobi: _mobile,
	            permission: _permission
	        },
	            success: function(data){
	                if(data.stat == "ok"){
						$("#js_save").attr('disable','disable');
						$("#js_save").addClass("notAllow");
	                    show_dialog_location_href("用户管理","保存成功！","/merchant/edit/listrole/");
	                    //window.location.href ="/merchant/edit/listrole/";
	                }else{
	                    show_dialog_none_reload("用户管理",data.msg);
	                }
	            },
	            error: function(){
	            }
			});
		})
	
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
	
	$(".change_passwd").click(function(){
	    if ($(this).html() == "重 置"){
	        $(this).html("取 消");
	        //$(this).parent().parent().find('div')[0].style.display="";
	        $("#show-pwd").css("display","inline-block");
	    }
	    else{
	        $(this).html("重 置");
	        //$(this).parent().parent().find('div')[0].style.display="none";
	        $("#show-pwd").css("display","none");
	        $("#m-pwd").val("");
	        $("#m-pwd1").val("");
	    }
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
	if($("#m-name").val() == ""){
		$("#m-name").focus().css("border","1px solid #f00");
		$(".name-error").html("姓名不能为空");
		return false;
	}
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


