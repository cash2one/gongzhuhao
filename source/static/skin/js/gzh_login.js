/**
 * Created by jane on 15/6/1.
 */
$(function(){
    var interVal;
    var count = 60;
    var curCount;
    var code = "";
    var codeLength = 4;

    $("#getCode").on("click", function(){
        curCount = count;
        var phone = $("#loginCodePhone").val();
        if(phone != ""){
            for (var i = 0; i < codeLength; i++){
                code += parseInt(Math.random() * 9).toString();
            }
            $("#getCode").attr("disabled","true");
            $("#getCode").val(curCount + "秒后重发");

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
                        $(".login-code-error").html(data.info);
                        return false;
                    }
                },

                error: function(){

                }
            });
        }else{
            $(".login-code-error").html("手机号码不能为空!");
            return false;
        }
    })

     function setRemainTime(){
        if(curCount == 0){
            window.clearInterval(interVal);
            $("#getCode").removeAttr("disabled");
            $("#getCode").val("重新获取验证码");
            code = "";
        }else{
            curCount --;
            $("#getCode").val(curCount + "秒后重发");
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

    $("#btnCodeLogin").on("click", function(){
        checkCodeForm();
        var phone = $("#loginCodePhone").val();
        var code = $("#loginCode").val();
        $.post('/api/login',{phone:phone,code:code},function(data){
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
                    alert("登录成功");
                  $('#phone_code_modal').modal('hide');
            }else{
                _html.html(obj.info);
                return false;
            }
        })
    })

    $("#btnPwdLogin").on("click", function(){
        checkForm();
        var phone = $("#loginPhone1").val();
        var pwd = $("#loginPwd").val();
        $.post('/api/login',{phone:phone,password:pwd},function(data){
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
                  $('#login_modal').modal('hide');

            }else{
                _html.html(obj.info);
                return false
            }
        })
    })


    function checkForm(e){
        if($("#loginPhone1").val() == ""){
            $('.error').html("手机号/用户名不能为空");
            $("#loginPhone1").focus();
            e.preventDefault();
            return false;
        }
        //if(!$("#loginPhone1").val().match(/^[1]\d{10}$/)){
        //   $(".error").html("手机格式不正确");
        //    $("#loginPhone1").focus();
        //   e.preventDefault();
        //    return false;
        //}
        if($("#loginPwd").val() == ""){
            $('.error').html("请填写您的密码");
            $("#loginPwd").focus();
            e.preventDefault();
            return false;
        }
    }

    function checkCodeForm(e){
        if($("#loginCodePhone").val() == ""){
            $('.error').html("手机号不能为空");
            $("#loginCodePhone").focus();
            e.preventDefault();
            return false;
        }
        if(!$("#loginCodePhone").val().match(/^[1]\d{10}$/)){
           $(".error").html("手机格式不正确");
            $("#loginCodePhone").focus();
           e.preventDefault();
            return false;
        }
        if($("#loginCode").val() == ""){
            $('.error').html("请输入4位验证码");
            $("#loginCode").focus();
            e.preventDefault();
            return false;
        }
    }

})