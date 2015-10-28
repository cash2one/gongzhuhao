/**
 * Created by jane on 15/6/1.
 */

$(function(){
	$(".input-txt").keyup(function(){
		$(".reg-error").html("");
	});
	$(".input-txt").blur(function(){
		$(".reg-error").html("");
	});
	$("#login, #register").click(function(){
		$(".reg-error").html("");
	});

	var interVal;
	var count = 60;
	var curCount;
	var code = "";
	var codeLength = 4;
    //var time_flag=0;
	$("#getRegCode").click(function(){
		curCount = count;
		var phone = $("#regPhone").val();
		if(phone != ""){
			for (var i = 0; i < codeLength; i++){
				code += parseInt(Math.random() * 9).toString();
			}

			$("#getRegCode").attr("disabled","true");
			$("#getRegCode").val(curCount + "秒后重发");

			interVal = window.setInterval(setRemainTime,1000);

			$.ajax({
				type: "get",
				dataType: "text",
				url:"/api/phone/code/" + phone + "/_code",
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
			window.clearInterval(interVal);
			$("#getRegCode").removeAttr("disabled");
			$("#getRegCode").val("重新获取验证码");
			code = "";
		}else{
			curCount --;
			$("#getRegCode").val(curCount + "秒后重发");
		}
	}

	var _html = $(".error");
	//输入区域输入状态下错误提示消失，文本框颜色改变
	$(".input-txt").keyup(function(){
		_html.html("");
	    $(this).css("border","1px solid #4cc25c");
	});
	$(".input-txt").blur(function(){
		_html.html("");
	    $(this).css("border","1px solid #d8d8d8");
	});

	$("#regSubmit").on('click',function(){
		checkRegForm();
		var phone = $("#regPhone").val();
		var code = $("#regCode").val();
        var password = $("#regPwd").val();

        if($('input[name = "agreement"]:checked').length < 0){
            alert("您还未选择《公主号用户协议》");
        }

        $.ajax({
				type: "put",
				dataType: "text",
				url:"/api/user/",
				data:{
					phone:phone,
                    code:code,
                    password:password
				},
				success: function(data){

                    var obj = $.parseJSON(data)
					if(obj.code == 200){
					    $('#head_url').attr('src',obj.data.user.Fphoto_url);
                         $('#nick_name').html(obj.data.user.Fnick_name);
                         $('#gzh-header-nav-normal').hide();
                         $('#gzh-header-nav').show();
                         window.login_user={
                            'nick':"'"+obj.data.user.Fnick_name+"'",
                            'id':"'"+obj.data.user.Fid+"'",
                            'uid':"'"+obj.data.user.Fuid+"'",
                            'head':"'"+obj.data.user.Fphoto_url+"'"
                        }
                        $('#register_modal').modal('hide');
					} else {
                        _html.html(obj.info);
                        return false;
                    }
				},

				error: function(){

				}
        })
	})

     function checkRegForm(e){
        if($("#regPhone").val() == ""){
            $('.error').html("手机号不能为空");
            $("#regPhone").focus();
            e.preventDefault();
            return false;
        }
        if(!$("#regPhone").val().match(/^[1]\d{10}$/)){
           $(".error").html("手机格式不正确");
            $("#regPhone").focus();
           e.preventDefault();
            return false;
        }
        if($("#regCode").val() == ""){
            $('.error').html("请输入4位验证码");
            $("#regCode").focus();
            e.preventDefault();
            return false;
        }
        if($("#regPwd").val() == ""){
            $('.error').html("请设置您的密码");
            $("#regPwd").focus();
            e.preventDefault();
            return false;
        }

        if($('input[name = "agreement"]:checked').length < 0){
            alert("您还未选择《公主号用户协议》");
        }

    }

})