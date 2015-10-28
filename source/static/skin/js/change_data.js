/**
 * Created by yijiaren-sun on 15-1-16.
 */
    $(document).ready(function () {
    var mobileRule = /^1\d{10}$/; //手机号的正则校验规则
    var mailRule =  /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;    //邮箱的正则校验规则


        //省的切换，带动市和区县的变化
    $('.province').change(function(){
        var province_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/location/province/change/"+province_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    loadSelect.addCity(data.city);
                    loadSelect.addCounty(data.area);
                }
            },
            error: function () {
            }
        });
    });

    //市的切换，带动区县的变化
    $('.city').change(function(){
        var city_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/location/area/"+city_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;
                stat == "ok" ? loadSelect.addCounty(data.list) : "";
            },
            error: function () {
            }
        });
    });

    var loadSelect = {
        addCity: function(city){    //加载市
            $('.city').empty();

            $.each(city, function(i){
                var option = '<option value="' + city[i].id + '">' + city[i].name + '</option>';
                $('.city').append(option);
            });
        },
        addCounty: function(area){    //加载县区
            $('.county').empty();

            $.each(area, function(i){
                var option = '<option value="' + area[i].id + '">' + area[i].name + '</option>';
                $('.county').append(option);
            });
        }
    };

        $('#change_phone').on('click', function () {
            $(this).addClass('hide');
            $("#phone,#phone_check_code").removeAttr('disabled');
            $('.phone-code-wrap').removeClass('hide');
        });

        $("#check_user").on('click', function () {
            name = $('#user_name').val();
            if (name == '') {
                alert('用户名称不能为空');
                return
            }
            $.get('/member/check/' + name, function (message) {
                if (message == 's') {
                    alert('用户可用');
                }
                else {
                    alert(message);
                }
            });
        });

        $('#birthday').datepicker({
            format: 'yyyy-mm-dd',
            startDate: '1900-01-01',
            endDate: '2014-12-12'
//                        startView: '1999-08-08'
        });
        $('#phone_send_code').on('click', function () {
            $('input[name="check_flag"]').val('true');
            var phone = $('#phone').val();
            if (phone == "" || !mobileRule.test(phone)) {
                    alert("联系电话为空或者格式不正确，请重新输入...");
                    return
                }
            var _xsrf = $('input[name="_xsrf"]').val();
            if($('.countDown').hasClass("hide")){
            jQuery.ajax({
                type: "POST",
                url: "/common/msg_send/change_data",
                data: {phone:phone, _xsrf:_xsrf},
                dataType: "JSON",
                success: function(data){
                    var stat = data.stat;

                    if(stat=="ok"){
                        $('.code-error-tips').text("");
                        $('.countDown').removeClass("hide");
                        countdown();
                    }else{
                        $('.code-error-tips').text(data.msg);
                    }
                },
                error: function(){

                }
            });
        }else{
            alert('请稍后在发!');
        }
        });

        $('.change-data-submit').click(function(){
//        var user_name = $('input[name="user_name"]').val().trim();
        var province = $('.province').val();
        var city = $('.city').val();
        var area = $('.county').val();
        var address = $('input[name="detail_address"]').val().trim();
        var nick = $('input[name="nick"] ').val().trim();
//        var phone = $('input[name="phone"]').val().trim();
//        var email = $('input[name="email"]').val().trim();
        var sex = $('input[name="sex"]:checked').val().trim();
        var sign_text = $('#sign_text').val();
        var _xsrf = $('input[name="_xsrf"]').val();
//        var real_name = $('input[name="real_name"]').val().trim();
//        var phone_check_code = $('input[name="phone_check_code"]').val().trim();
//        var check_flag = $('input[name="check_flag"]').val().trim();
        var result = true;     //全局保存判断
            if(result ){
                if(nick == "" || nick.length >20) {
                    result = false;
                    alert("昵称不能为空且不能超过20字符");
                }
        }
//        if(result && email != ""){
//            if(!mailRule.test(email)){
//                result = false;
//                alert("邮箱格式不正确，请重新输入...");
//            }
//        }
//        if(result && phone !=""){
//            if(!mobileRule.test(phone)){
//                result = false;
//                alert("手机格式不正确，请重新输入...");
//            }
//        }
//        if(result && check_flag == 'true'){
//            if(phone_check_code == ""){
//                result = false;
//                alert("验证码不能为空！");
//            }
//        }
        if(result){
            var data_list = new Object();

//            data_list.user_name = user_name;
            data_list.province = province;
            data_list.city = city;
            data_list.area = area;
            data_list.detail_address = address;
            data_list.nick = nick;
//            if (phone_check_code!=""){
//               data_list.phone = phone;
//               data_list.phone_check_code = phone_check_code;
//            }
//            data_list.email = email;
            data_list.sex = sex;
            data_list.sign_text = sign_text;
//            data_list.real_name = real_name;
            data_list._xsrf = _xsrf;

            jQuery.ajax({
                type: "POST",
                url: window.location.href,
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        alert('保存成功');
                        window.location.href = '/member/index/'+data.id;
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        }
    });

    });
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

