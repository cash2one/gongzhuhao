/**
 * Created by hujunhao on 14/12/8.
 */
//    changed by mele on 15/01/28

//全局变量判断
var v = {
    mobile: "",     //手机号
    code: "",       //验证码
    password: "",   //密码
    nickname: ""   //确认密码
}

//错误文案
var errorMessage = {
        mobileNone: "请输入手机号！",
        mobileError: " 手机号有误，请重新输入！",
        sendCodeError: "请求发送验证码失败，情检查手机号是否正确！",
        sendTooFastError: "请稍后在发！",
        codeNone: "验证码不能为空！",
        pswNone: "密码不能为空!",
        pswError: "密码的长度为6~12位!",
        psw2None: "确认密码不能为空!",
        psw2Error: "密码不一致!"
    },
    message = $(".message");

//页面配置信息
var configuration = {
    mobileReg:  /^[1]\d{10}$/  //手机号正则校验规则
}

var inputInfo = {
    operating: function() {
        //手机号在此校验
        $('#J-mobile').change(function () {
            checkInfo.checkMobile();
        });

        //发送验证码
        $('#J-send-ok').click(function(){
            if(checkInfo.checkMobile()){
                var mobile = $('#J-mobile').val();
                var _xsrf = $('input[name="_xsrf"]').val();
                checkInfo.sendCode(mobile, _xsrf);
            }else{
                message.text(errorMessage.sendCodeError);
            }
        });

        //验证码输入
        $('#J-verificationcode').change(function () {
            checkInfo.checkCode();
        });

        //密码
        $('#J-password').change(function(){
            checkInfo.checkPsw();
        });

        //确认密码
        $('#J-password2').change(function(){
            checkInfo.checkPsw2();
        });

        //提交注册页面
        $('.reg-btn').click(function(){
            var m = checkInfo.checkMobile();
            var c = checkInfo.checkCode();
            var p = checkInfo.checkPsw();
//                var p2 = checkInfo.checkPsw2();

            if(m && c && p) {
                if(document.getElementById("J-agreement").checked) {
                    v.nickname = $('#J-nickname').val();
                    var _xsrf = $('input[name="_xsrf"]').val();
                    var img_check_juage = $('input[name="img_check"]').val();
                    var _url = $('input[name="_url"]').val();
                    v.password = $('#J-password').val();

                    if(img_check_juage=="False"){
                        jQuery.ajax({
                            type: "POST",
                            url: "/member/reg",
                            data: {phone: v.mobile, phone_check_code: v.code, password: v.password, nick: v.nickname, _xsrf:_xsrf},
                            dataType: "JSON",
                            success: function(data){
                                var stat = data.stat;

                                if(stat=="ok"){
                                    window.location.href = _url;
                                }else{
                                    message.text(data.msg);
                                }
                            },
                            error: function(){

                            }
                        });
                    }else if(img_check_juage=="True"){
                        var img_check = $('#img_check_code').val();
                        img_check = img_check.trim();

                        if(img_check!=""){
                            $('.icc-error-tips').text("");
                            jQuery.ajax({
                                type: "POST",
                                url: "/member/reg",
                                data: {phone: v.mobile, phone_check_code: v.code, password: v.password, img_check_code: img_check, nick: v.nickname, _xsrf:_xsrf},
                                dataType: "JSON",
                                success: function(data){
                                    var stat = data.stat;

                                    if(stat=="ok"){
                                        window.location.href = _url;
                                    }else{
                                        message.text(data.msg);
                                    }
                                },
                                error: function(){

                                }
                            });
                        }else{
                            message.text(errorMessage.codeNone);
                        }
                    }
                } else {
                    message.text("请仔细阅读《怎么装网站注册协议》，并同意！");
                }
            }
        });
    }
}

var checkInfo = {
    checkMobile: function(){
        var mobile = $('#J-mobile').val();
        mobile = mobile.trim();
        var length = mobile.length;
        if(length!=0){
            if(configuration.mobileReg.test(mobile)){
                message.text("");
                v.mobile = mobile;
                return true;
            }else{
                message.text(errorMessage.mobileError);
                v.mobile = "";
                return false;
            }
        }else{
            message.text(errorMessage.mobileNone);
            v.mobile = "";
            return false;
        }
    },
    sendCode: function(mobile, _xsrf){
        if($('.countDown').hasClass("hide")){
            jQuery.ajax({
                type: "POST",
                url: "/common/msg_send/reg",
                data: {phone:mobile, _xsrf:_xsrf},
                dataType: "JSON",
                success: function(data){
                    var stat = data.stat;

                    if(stat=="ok"){
                        message.text("");
                        $('.countDown').removeClass("hide");
                        countdown();
                    }else{
                        message.text(data.msg);
                    }
                },
                error: function(){

                }
            });
        }else{
            message.text(errorMessage.sendTooFastError);
        }
    },
    checkCode: function(){
        var code = $('#J-verificationcode').val();
        code = code.trim();

        if(code==""){
            message.text(errorMessage.codeNone);
            v.code = "";
            return false;
        }else{
            message.text("");
            v.code = code;
            return true;
        }
    },
    checkPsw: function(){
        var psw = $('#J-password').val();
        psw = psw.trim();
        var length = psw.length;

        if(length!=0){
            if(length>=6 && length<=12){
                message.text("");
                return true;
            }else{
                message.text(errorMessage.pswError);
                return false;
            }
        }else{
            message.text(errorMessage.pswNone);
            return false;
        }
    },
    checkPsw2: function(){
        var psw2 = $('#J-password2').val();
        psw2 = psw2.trim();
        var psw = $('#J-password').val();
        var length = psw2.length;

        if(length!=0){
            if(psw==psw2){
                message.text("");
                v.password = psw;
                return true;
            }else{
                message.text(errorMessage.psw2Error);
                v.password = "";
                return false;
            }
        }else{
            message.text(errorMessage.psw2None);
            v.password = "";
            return false;
        }
    }
}

//倒计时
function countdown(){
    var time = parseInt($('#lastTime').text())-1;

    if(time==0){
        clearTimeout(Account);
        $('#lastTime').html("60");
        $('.countDown').addClass("hide");
    }else{
        $('#lastTime').text(time);
        var Account = setTimeout("countdown()",1000);
    }
}


$(document).ready(function(){
    //替换图形验证码
    $('.img-code').click(function(){
        var old_src = $(this).attr("src");
        var src = old_src.split("?")[0];
        var date = new Date();
        var new_src = src + "?" + date.getTime();
        $(this).attr("src", new_src);
    });
});

/**
 * Created by hujunhao on 14/12/8.
 */

//全局变量判断
var v = {
        mobile: "",     //手机号
        code: "",       //验证码
        password: "",   //密码
        nickname: ""   //确认密码
    }

//错误文案
var errorMessage = {
        mobileNone: "请输入手机号！",
        mobileError: " 手机号有误，请重新输入！",
        sendCodeError: "请求发送验证码失败，情检查手机号是否正确！",
        sendTooFastError: "请稍后在发！",
        codeNone: "验证码不能为空！",
        pswNone: "密码不能为空!",
        pswError: "密码的长度为6~12位!",
        psw2None: "确认密码不能为空!",
        psw2Error: "密码不一致!"
    },
    message = $(".message");

//页面配置信息
var configuration = {
    mobileReg:  /^[1]\d{10}$/  //手机号正则校验规则
}

var inputInfo = {
    operating: function() {
        //手机号在此校验
        $('#J-mobile').change(function () {
            checkInfo.checkMobile();
        });

        //发送验证码
        $('#J-send-ok').click(function(){
            if(checkInfo.checkMobile()){
                var mobile = $('#J-mobile').val();
                var _xsrf = $('input[name="_xsrf"]').val();
                checkInfo.sendCode(mobile, _xsrf);
            }else{
                message.text(errorMessage.sendCodeError);
            }
        });

        //验证码输入
        $('#J-verificationcode').change(function () {
            checkInfo.checkCode();
        });

        //密码
        $('#J-password').change(function(){
            checkInfo.checkPsw();
        });

        //确认密码
        $('#J-password2').change(function(){
            checkInfo.checkPsw2();
        });

        //提交注册页面
        $('.reg-btn').click(function(){
            var m = checkInfo.checkMobile();
            var c = checkInfo.checkCode();
            var p = checkInfo.checkPsw();
//                var p2 = checkInfo.checkPsw2();

            if(m && c && p) {
                if(document.getElementById("J-agreement").checked) {
                    v.nickname = $('#J-nickname').val();
                    var _xsrf = $('input[name="_xsrf"]').val();
                    var img_check_juage = $('input[name="img_check"]').val();
                    var _url = $('input[name="_url"]').val();
                    v.password = $('#J-password').val();

                    if(img_check_juage=="False"){
                        jQuery.ajax({
                            type: "POST",
                            url: "/member/reg",
                            data: {phone: v.mobile, phone_check_code: v.code, password: v.password, nick: v.nickname, _xsrf:_xsrf},
                            dataType: "JSON",
                            success: function(data){
                                var stat = data.stat;

                                if(stat=="ok"){
                                    window.location.href = _url;
                                }else{
                                    message.text(data.msg);
                                }
                            },
                            error: function(){

                            }
                        });
                    }else if(img_check_juage=="True"){
                        var img_check = $('#img_check_code').val();
                        img_check = img_check.trim();

                        if(img_check!=""){
                            $('.icc-error-tips').text("");
                            jQuery.ajax({
                                type: "POST",
                                url: "/member/reg",
                                data: {phone: v.mobile, phone_check_code: v.code, password: v.password, img_check_code: img_check, nick: v.nickname, _xsrf:_xsrf},
                                dataType: "JSON",
                                success: function(data){
                                    var stat = data.stat;

                                    if(stat=="ok"){
                                        window.location.href = _url;
                                    }else{
                                        message.text(data.msg);
                                    }
                                },
                                error: function(){

                                }
                            });
                        }else{
                            message.text(errorMessage.codeNone);
                        }
                    }
                } else {
                    message.text("请仔细阅读《怎么装网站注册协议》，并同意！");
                }
            }
        });
    }
}

var checkInfo = {
    checkMobile: function(){
        var mobile = $('#J-mobile').val();
        mobile = mobile.trim();
        var length = mobile.length;
        if(length!=0){
            if(configuration.mobileReg.test(mobile)){
                message.text("");
                v.mobile = mobile;
                return true;
            }else{
                message.text(errorMessage.mobileError);
                v.mobile = "";
                return false;
            }
        }else{
            message.text(errorMessage.mobileNone);
            v.mobile = "";
            return false;
        }
    },
    sendCode: function(mobile, _xsrf){
        if($('.countDown').hasClass("hide")){
            jQuery.ajax({
                type: "POST",
                url: "/common/msg_send/reg",
                data: {phone:mobile, _xsrf:_xsrf},
                dataType: "JSON",
                success: function(data){
                    var stat = data.stat;

                    if(stat=="ok"){
                        message.text("");
                        $('.countDown').removeClass("hide");
                        countdown();
                    }else{
                        message.text(data.msg);
                    }
                },
                error: function(){

                }
            });
        }else{
            message.text(errorMessage.sendTooFastError);
        }
    },
    checkCode: function(){
        var code = $('#J-verificationcode').val();
        code = code.trim();

        if(code==""){
            message.text(errorMessage.codeNone);
            v.code = "";
            return false;
        }else{
            message.text("");
            v.code = code;
            return true;
        }
    },
    checkPsw: function(){
        var psw = $('#J-password').val();
        psw = psw.trim();
        var length = psw.length;

        if(length!=0){
            if(length>=6 && length<=12){
                message.text("");
                return true;
            }else{
                message.text(errorMessage.pswError);
                return false;
            }
        }else{
            message.text(errorMessage.pswNone);
            return false;
        }
    },
    checkPsw2: function(){
        var psw2 = $('#J-password2').val();
        psw2 = psw2.trim();
        var psw = $('#J-password').val();
        var length = psw2.length;

        if(length!=0){
            if(psw==psw2){
                message.text("");
                v.password = psw;
                return true;
            }else{
                message.text(errorMessage.psw2Error);
                v.password = "";
                return false;
            }
        }else{
            message.text(errorMessage.psw2None);
            v.password = "";
            return false;
        }
    }
}

//倒计时
function countdown(){
    var time = parseInt($('#lastTime').text())-1;

    if(time==0){
        clearTimeout(Account);
        $('#lastTime').html("60");
        $('.countDown').addClass("hide");
    }else{
        $('#lastTime').text(time);
        var Account = setTimeout("countdown()",1000);
    }
}


$(document).ready(function(){
    //替换图形验证码
    $('.img-code').click(function(){
        var old_src = $(this).attr("src");
        var src = old_src.split("?")[0];
        var date = new Date();
        var new_src = src + "?" + date.getTime();
        $(this).attr("src", new_src);
    });
});