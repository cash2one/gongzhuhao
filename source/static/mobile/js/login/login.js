
$(function(){
	$("#nav a:first,#con .con-item:first").addClass("on");
	$("#nav a").each(function(i){
		$(this).click(function(){
			$(this).addClass("on").parent().siblings().find("a").removeClass("on");
			$($("#con .con-item")[i]).show().siblings().hide();
		});
	});	
	
	$("#login").click(function(){
		checkForm();
	    $("#user_login_form").submit();
	})
})

function checkForm(){
	
	if($("#mobile").val() == ""){
		$(".mobile-error").html("请输入您的手机号");
		$("#mobile").focus();
		return false;
	}
	//if(!$("#mobile").val().match(/^(((13[0-9]{1})|159|153)+\d{8})$/)){
	//	$(".mobile-error").html("手机号码输入不正确");
	//	$("#mobile").focus();
	//	return false;
	//}
	
	if($("#password").val() == ""){
		$(".pwd-error").html("请输入密码");
		$("#password").focus();
		return false;
	}
	
	$(".input-txt").keyup(function(){
		$(this).closest(".ul-setting").find(".error").html("");
	});	
	$(".input-txt").blur(function(){
		$(this).closest(".ul-setting").find(".error").html("");
	});
	$("#login").click(function(){
		$(this).closest(".ul-setting").find(".error").html("");
	});	
}
