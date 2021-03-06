
$(function(){
	$("#nav a:first,#con .con-item:first").addClass("on");
	$("#nav a").each(function(i){
		$(this).click(function(){
			$(this).addClass("on").parent().siblings().find("a").removeClass("on");
			$($("#con .con-item")[i]).show().siblings().hide();
		});
	});	

	$(".input-txt").keyup(function(){
		$(".reg-error").html("");
	});	
	$(".input-txt").blur(function(){
		$(".reg-error").html("");
	});
	$("#login, #register").click(function(){
		$(".reg-error").html("");
	});	
	
	$("#login").click(function(){
		checkForm();
	    $("#user_login_form").submit();
	});
	
	
	var interVal; 
	var count = 60; 
	var curCount;
	var code = "";
	var codeLength = 4;	
	
	$("#sendCode").click(function(){
		curCount = count;
		var phone = $("#phone").val();
		if(phone != ""){
			for (var i = 0; i < codeLength; i++){
				code += parseInt(Math.random() * 9).toString();
			}
			
			$(".btn-code").attr("disabled","true");
			$(".btn-code").addClass("notAllow");
			
			$(".btn-code").val(curCount + "秒后重发");
			
			interVal = window.setInterval(setRemainTime,1000);
			
			$.ajax({
				type: "get",
				dataType: "text",
				url:"/mobile/phone/send_phone_code/",
				data:{
					phone: phone
				},
				success: function(data){
					if(data.stat != "1000"){
						$(".reg-error").html(data.info);
			            return false;
					}
				},

				error: function(){

				}
			});
		}else{
			$(".reg-error").html("手机号码不能为空!");
			return false;
		}		
	})
	
	function setRemainTime(){
		if(curCount == 0){
			window.clearInterval();
			$(".btn-code").removeAttr("disabled");
			$(".btn-code").removeClass("notAllow");
			$(".btn-code").val("重新获取验证码");
			code = "";
		}else{
			curCount --;
			$(".btn-code").val(curCount + "秒后重发");
		}
	}	
	
	
	$("#register").click(function(){
		checkForm();
		var phone = $("#phone").val();
		var code = $("#code").val();
		
		$.ajax({
			type: "post",
			url:"/mobile/phone/reg/",
			data:{
				phone: phone,
				code: code
			},
			success: function(data){
				var obj = $.parseJSON(data)
				if(obj.stat == "1000"){
					window.location.href = obj.url;
				}else{
					$("error").html(data.info);
                    $("#code").focus();
                    return false;
				}
			},
	
			error: function(){
			}
		});
	})	
	
})

function checkForm(){
	
	if($("#mobile").val() == ""){
		$("error").html("请输入您的手机号");
		$("#mobile").focus();
		return false;
	}
	
	if($("#password").val() == ""){
		$("error").html("请输入密码");
		$("#password").focus();
		return false;
	}
}
