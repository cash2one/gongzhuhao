$(document).ready(function(){
    var mobileRule = /^1\d{10}$|^(0\d{2,3}-?|\(0\d{2,3}\))?[1-9]\d{4,7}(-\d{1,8})?$|^400-?\d{3}-?\d{4}$/; //手机号的正则校验规则
    var mailRule =  /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;    //邮箱的正则校验规则
    var qqRule = /^[1-9][0-9]{4,14}$/;  //QQ的正则校验规则

    //添加电话
    //$('.add-phone-btn').click(function(){
    //    var htmls = $('#J-model-phone').html();
    //    $('.phone-list').append(htmls)
    //});

    //$('.phone-list').on('click', '.del-phone-btn',function(){
    //    $(this).closest(".basic-info-list").remove();
    //});

    //省的切换，带动市和区县的变化
    $('.province').change(function(){
        var province_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/merchant/edit/province/"+province_id+"/",
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
            url: "/merchant/edit/city/"+city_id+"/",
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
                var option = '<option value="' + city[i].Fid + '">' + city[i].Fcity_name + '</option>';
                $('.city').append(option);
            });
        },
        addCounty: function(area){    //加载县区
            $('.county').empty();

            $.each(area, function(i){
                var option = '<option value="' + area[i].Fid + '">' + area[i].Farea_name + '</option>';
                $('.county').append(option);
            });
        }
    }

    $('input[name="company_name"]').change(function(){
        var name = $(this).val();
        name!="" ? $('.company-name-err').text("") : $('.company-name-err').text("公司名称不能为空！");
    });
    $('input[name="detail_address"]').change(function(){
        var address = $(this).val();
        address!="" ? $('.detail-address-err').text("") : $('.detail-address-err').text("详细地址不能为空！");
    });
    $('input[name="contacts"]').change(function(){
        var contact = $(this).val();
        contact!="" ? $('.contacts-err').text("") : $('.contacts-err').text("联系人不能为空！");
    });
    $('.phone-list').on('change', 'input[name="contacts_tel"]',function(){
        var phone = $(this).val();
        if(phone==""){
            $(this).siblings('.contacts-tels-err').text("联系电话不能为空！")
        }
        /**
        else{
            if(mobileRule.test(phone)){
                $(this).siblings('.contacts-tels-err').text("");
            }else{
                $(this).siblings('.contacts-tels-err').text("联系电话格式不正确！")
            }
        }
        */
    });
    $('input[name="mail"]').change(function(){
        var mail = $(this).val();
        if(mail==""){
            $('.mail-err').text("邮箱不能为空！")
        }else{
            if(mailRule.test(mail)){
                $('.mail-err').text("");
            }else{
                $('.mail-err').text("邮箱格式不正确！")
            }
        }
    });

	$(".input-txt").keyup(function(){
		$(this).closest(".company").find(".error").html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	
	$(".input-txt").blur(function(){
		$(this).closest(".company").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
	
	$(".basic-info-save-btn").click(function(){
		$(this).closest(".company").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});

    $('.basic-info-save-btn').click(function(){
        var name = $('input[name="company_name"]').val();
        var province = $('#province option:selected').val();
        var city = $('#city option:selected').val();
        var area = $('#county option:selected').val();
        var address = $('input[name="detail_address"]').val();
        var contact = $('input[name="contacts"]').val();
        var phone = new Array();
        $('input[name="contacts_tel"]').each(function(){
            phone.push($(this).val());
        });
        var qq = $('input[name="qq"]').val();
        var mail = $('input[name="mail"]').val();
        var desc = $('#desc').val();
        var photo_url = $('input[name="Fphoto_url"]').val();
        var _xsrf = $('input[name="_xsrf"]').val();

        var result = true;     //全局保存判断

        if(name==""){
            result = false;
            $("#company_name").focus().css("border","#1px solid #f00");
            $(".company-error").html("请填写公司名称")
        }
        if(result){
            if(province=="" || province=="0"){
                result = false;
                $("#province").focus().css("border","#1px solid #f00");
                $(".province-error").html("请选择省份！");
            }
            if(city=="" || city=="0"){
                result = false;
                $("#city").selected().css("border","#1px solid #f00");
                $(".province-error").html("请选择市！");
            }
            if(area=="" || area=="0"){
                result = false;
                $("#county").focus().css("border","#1px solid #f00");
                $(".province-error").html("请选择县，区！");
            }
        }
        if(result){
            if(address==""){
                result = false;
                $("#detail_address").focus().css("border","#1px solid #f00");
                $(".address-error").html("请填写详细地址！");
            }
        }
        if(result){
            if(contact==""){
                result = false;
                $("#contacts").focus().css("border","#1px solid #f00");
                $(".contacts-error").html("请填写联系人！");
            }
        }
//        if(result){
//            for (i in phone) {
//                if (phone[i] == "" || !mobileRule.test(phone[i])) {
//                    result = false;
//                    $("#contacts_tel").focus().css("border","#1px solid #f00");
//                    $(".tel-error").html("联系电话为空或者格式不正确，请重新输入...");
//                }
//            }
//        }
//       if(result){
//          if(qq=="" || !qqRule.test(qq)){
//              result = false;
//              $("#qq").focus().css("border","#1px solid #f00");
//              $(".qq-error").html("QQ为空或格式不正确，请重新输入...");
//          }
//      }
//      if(result){
//          if(mail=="" || !mailRule.test(mail)){
//              result = false;
//              $("#mail").focus().css("border","#1px solid #f00");
//              $(".mail-error").html("邮箱为空或者格式不正确，请重新输入...");
//          }
//      }
        if(result){
            var desc_length = desc.length;
            if(desc_length>300){
                result = false;
                alert("描述内容"+desc_length+"个字，请删减到300个字！");
            };
        }
//      if(result){
//          if(photo_url==""){
//              result = false;
//				$(".logo-error").html("请上传LOGO");
//          }
//      }
        if(result){
            var data_list = new Object();

            data_list.Fcompany_name = name;
            data_list.Fprovince = province;
            data_list.Fcity = city;
            data_list.Farea = area;
            data_list.Fdetail_address = address;
            data_list.Fcontact = contact;
            data_list.Fphone = phone.join(',');
            data_list.Fqq = qq;
            data_list.Fmail = mail;
            data_list.Fdescription = desc;
            data_list.Fphoto_url = photo_url;
            data_list._xsrf = _xsrf;

            jQuery.ajax({
                type: "POST",
                url: "/merchant/edit/",
                data: data_list,
                //dataType: "JSON",
                success: function (data) {
                    //var stat = data.stat;
                    data = $.parseJSON(data);
                    if (data.stat == "ok") {
                        $(".basic-info-save-btn").attr('disable','disable');
                        $(".basic-info-save-btn").addClass("notAllow");
                        show_dialog_reload("修改商户信息","修改成功！");
                    } else {
                        show_dialog_reload("修改商户信息",data.msg);
                    }
                },
                error: function () {
                }
            });
        }
    });

});
