/**
 * Created by hujunhao on 14/12/13.
 */


$(document).ready(function(){
    
    $('input[name="old_pwd"]').change(function(){
        var old_pwd = $(this).val().trim();
        if(old_pwd==""){
            errCheck("old_pwd", false, "原密码不能为空！");
        }else{
            errCheck("old_pwd", true, "");
        }
    });

    $('input[name="new_pwd"]').change(function(){
        var old_pwd = $('input[name="old_pwd"]').val().trim();
        var new_pwd = $(this).val().trim();

        if(old_pwd==""){
            errCheck("old_pwd", false, "原密码不能为空！");
        }else{
            if(new_pwd==""){
                errCheck("new_pwd", false, "新密码不能为空！");
            }else{
                if(new_pwd==old_pwd){
                    errCheck("new_pwd", false, "新密码不能和原密码一样！");
                }else{
                    errCheck("new_pwd", true, "");
                }
            }
        }
    });

    $('input[name="confirm_pwd"]').change(function(){
        var new_pwd = $('input[name="new_pwd"]').val().trim();
        var confirm_pwd = $(this).val().trim();

        if(new_pwd==""){
            errCheck("new_pwd", false, "新密码不能为空！");
        }else{
            if(confirm_pwd==""){
                errCheck("confirm_pwd", false, "确认密码不能为空！");
            }else{
                if(new_pwd!=confirm_pwd){
                    errCheck("confirm_pwd", false, "确认密码必须要和新密码一致！");
                }else{
                    errCheck("confirm_pwd", true, "");
                }
            }
        }
    });

    $('.modify-save-btn').click(function(){
        var old_pwd = $('input[name="old_pwd"]').val().trim();
        var new_pwd = $('input[name="new_pwd"]').val().trim();
        var confirm_pwd = $('input[name="confirm_pwd"]').val().trim();
        var _xsrf = $('input[name="_xsrf"]').val();

        if(old_pwd==""){
            errCheck("old_pwd", false, "原密码不能为空！");
        }else{
            if(new_pwd=="" || new_pwd==old_pwd){
                errCheck("new_pwd", false, "请重新输入新密码，并确保与原密码不一致！");
            }else{
                if(confirm_pwd=="" || confirm_pwd!=new_pwd){
                    errCheck("confirm_pwd", false, "请重新输入确认密码，并确保与新密码一致！");
                }else{
                    jQuery.ajax({
                        type: "POST",
                        url: "/member/pwd",
                        data: {old_pwd:old_pwd, new_pwd:new_pwd, new_pwd_confirm:confirm_pwd, _xsrf:_xsrf},
                        dataType: "JSON",
                        success: function(data){
                            var stat = data.stat;

                            if(stat=="ok"){
                                alert("修改成功！");
                                window.location.href = '/merchant/index/product'
                            }else{
                                alert(data.msg);
                            }
                        },
                        error: function(){

                        }
                    });
                }
            }
        }

    });

    function errCheck(type, juage, msg){
        switch(type){
            case "old_pwd":
                $('.old-pwd-err').text(juage ? "" : msg);
                break;
            case "new_pwd":
                $('.new-pwd-err').text(juage ? "" : msg);
                break;
            case "confirm_pwd":
                $('.new-confirm-pwd-err').text(juage ? "" : msg);
                break;
        }
    }
});