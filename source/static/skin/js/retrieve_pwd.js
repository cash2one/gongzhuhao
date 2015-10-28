/**
 * Created by hujunhao on 14/12/25.
 */

$(document).ready(function(){
    // 规则
    var rule = {
        mobileRule: /^[1]\d{10}$/ //手机号的正则校验规则
    }
    //post请求必要参数
    var _xsrf = $('input[name="_xsrf"]').val();

    //替换图形验证码
    $('.change-code').click(function(){
        var old_src = $('.code-img').attr("src");
        var src = old_src.split("?")[0];
        var date = new Date();
        var new_src = src + "?" + date.getTime();
        $('.code-img').attr("src", new_src);
    });

    //注册手机号校验
    $('input[name="phone"]').change(function(){
        check.phone();
    });

    //发送手机验证码
    $('.send-code').click(function(){
        var _self = $(this);
        var status = _self.attr("data-status");
        if(status=="true"){
            var phone = $('input[name="_mobile"]').val();

            jQuery.ajax({
                type: "POST",
                url: "/common/msg_send/retrieve_pwd",
                data: {phone:phone, _xsrf:_xsrf},
                dataType: "JSON",
                success: function(data){
                    var stat = data.stat;

                    if(stat=="ok"){
                        $('.phoneCodeErr').text()!="" ? $('.phoneCodeErr').empty() : "";
                        _self.attr("data-status", "false");
                        $('.countDown').removeClass("hide");
                        countdown();
                    }else{
                        $('.phoneCodeErr').text(data.msg);
                    }
                },
                error: function(){

                }
            });
        }else{
            $('.phoneCodeErr').text("请"+$('#lastTime').text()+"秒后再发送！");
        }
    });

    //密码
    $('#J-password').change(function(){
        check.checkPsw();
    });
    //确认密码
    $('#J-password2').change(function(){
        check.checkPsw2();
    });

    //第一步提交操作
    $('.first-step-btn').click(function(){
        var phone = check.phone();

        if(phone){
            var img_check_code = $('input[name="img_check_code"]').val();

            if(img_check_code!=""){
                var data_list = new Object();
                data_list.phone = phone;
                data_list.img_check_code = img_check_code;
                data_list._xsrf = _xsrf;
                data_list.step = "1";

                nextTo(data_list);
            }
        }
    });

    //第二步提交操作
    $('.second-step-btn').click(function(){
        var phone = $('input[name="_mobile"]').val();
        var phone_check_code = $('input[name="phone_check_code"]').val();

        if(phone_check_code!=""){
            var data_list = new Object();
            data_list.phone = phone;
            data_list.phone_check_code = phone_check_code;
            data_list._xsrf = _xsrf;
            data_list.step = "2";

            nextTo(data_list);
        }
    });

    //第三步提交操作
    $('.third-step-btn').click(function(){
        var phone = $('input[name="_mobile"]').val();
        var new_pwd = $('#J-password').val();
        var new_pwd_confirm = $('#J-password2').val();

        if(check.checkPsw() && check.checkPsw2()){
            var data_list = new Object();
            data_list.phone = phone;
            data_list.new_pwd = new_pwd;
            data_list.new_pwd_confirm = new_pwd_confirm;
            data_list._xsrf = _xsrf;
            data_list.step = "3";

            nextTo(data_list);
        }
    });

    function nextTo(data_list){

        jQuery.ajax({
            type: "POST",
            url: "/member/retrieve/pwd",
            data: data_list,
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;

                if(stat=="ok") {
                    if(data_list.step=="1"){
                        $('input[name="_mobile"]').attr("value", data_list.phone);
                        $('.part_1').addClass("hide");
                        $('.part_2').removeClass("hide");
                    }else if(data_list.step=="2"){
                        $('.part_2').addClass("hide");
                        $('.part_3').removeClass("hide");
                        $('.phoneCodeErr').empty();
                    }else if(data_list.step=="3") {
                        alert("修改成功！");
                        window.location.href = "/";
                    }
                }else if(stat=="forbid"){
                    check.back();
                }else{
                    alert(data.msg);
                }
            },
            error: function(){

            }
        });
    }

    var check = {
        phone: function(){
            var phone = $('input[name="phone"]').val();
            if(rule.mobileRule.test(phone)){
                $('.phoneErr').empty();
                return phone;
            }else{
                $('.phoneErr').text("注册手机号格式有误，请重输...");
                $('input[name="phone"]').focus();
                return false;
            }
        },
        checkPsw: function(){
            var psw = $('#J-password').val();
            var length = psw.length;

            if(length!=0){
                if(length>=6 && length<=12){
                    $('.pwdErr').text("");
                    return true;
                }else{
                    $('.pwdErr').text("密码的长度为6~12位!");
                    return false;
                }
            }else{
                $('.pwdErr').text("密码不能为空!");
                return false;
            }
        },
        checkPsw2: function(){
            var psw2 = $('#J-password2').val();
            var psw = $('#J-password').val();
            var length = psw2.length;

            if(length!=0){
                if(psw==psw2){
                    $('.pwd2Err').text("");
                    return true;
                }else{
                    $('.pwd2Err').text("密码不一致!");
                    return false;
                }
            }else{
                $('.pwd2Err').text("确认密码不能为空!");
                return false;
            }
        },
        back: function(){
            $('.part').each(function(i){
                if(i==0){
                    $(this).hasClass("hide") ? $(this).removeClass("hide") : "";
                }else{
                    $(this).hasClass("hide") ? "" : $(this).addClass("hide");
                }
            });
            $('.put-in').val(""), $('.put-in2').val("");
        }
    }
    //倒计时
    function countdown(){
        var time = parseInt($('#lastTime').text())-1;

        if(time==0){
            clearTimeout(Account);
            $('#lastTime').html("60");
            $('.countDown').addClass("hide");
            $('.send-code').attr("data-status", "true");
            $('.phoneCodeErr').text()!="" ? $('.phoneCodeErr').empty() : "";
        }else{
            $('#lastTime').text(time);
            var Account = setTimeout(function(){
                countdown();
            },1000);
        }
    }
});