/**
 * Created by mele on 15/1/23.
 */
//reserveModal
var check_url = $("input[name='check_url']").val();
var post_url = $("input[name='post_url']").val();
function reserve(btn){
    btn.click(function(e){
        e.preventDefault();
        if($("#is_login").val() == "0"){
            $("#J-login").trigger("click");
        }else{
            //判断是否已预约
            $("#reserveModal").modal();
        }
    })
}
//close > clear
$("#reserveModal .close").click(function(){
    $("#reserveModal").find("textarea,input:not(input[type='submit'])").val("");
})

//reserve_submit
$(".reserve-submit").click(function(e){
    e.preventDefault();
    var formData = $("#exchange_form").serializeArray();
    trim_reserve(formData);
    if(!$(".reserve-error").hasClass("error")){
        var data = serializeData(formData);
        $.ajax({
            url: $('#exchange_form').attr('action'),
            data: data,
            dataType: "json",
            beforeSend: function(){
                $('.reserve-submit').val("正在提交...");
            },
            success: function(response){
                if(response.state == "ok"){
                    $(".reserve-modal-body").hide();
                    $(".success-message").removeClass("hide");
                }else{
                    $(".reserve-error").removeClass("hide").text(response.error);
                    $('.reserve-submit').val("");
                }
            },
            error: function(error){
                console.log(error);
            }
        })
    }
})
//校验
function trim_reserve(formData){
    $.each(formData,function(item){
        var o = formData[item];
        if(o.name == "username"){
            if(!trim_empty(o)) return false;
        }else if(o.name == "tel"){
            if(!trim_empty(o)) return false;
            var val = formData[item].value;
            if(! /^[1]\d{10}$/.test(val)){
                $(".reserve-error").text("手机号码格式不正确。").removeClass("hide").addClass("error");
                return false;
            }else {
                $(".reserve-error").text("").removeClass("error").addClass("hide");
            }
        }else if(o.name == "area"){
            if(!trim_empty(o)) return false;
        }
    });
}
//校验非空
function trim_empty(o){
    if(o.value == ""){
        if(o.name == "username"){
            var message = "您的称呼必须要填哦";
        }else if(o.name == "tel"){
            var message = "手机号码必须要填哦";
        }
        $(".reserve-error").text("*"+message).removeClass("hide").addClass("error");
        return false;
    }else{
        return true;
    }
}
//序列表单为json
function serializeData(o){
    if(o){
        var O = {};
        $.each(o,function(i){
            var oi = o[i];
            O[oi["name"]] = oi["value"];
        });
        return O;
    }
}