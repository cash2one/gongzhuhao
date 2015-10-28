/**
 * Created by hujunhao on 14/12/13.
 */

$(document).ready(function(){
    var mobileRule = /^1\d{10}$|^(0\d{2,3}-?|\(0\d{2,3}\))?[1-9]\d{4,7}(-\d{1,8})?$|^400-?\d{3}-?\d{4}$/; //手机号的正则校验规则
    var mailRule =  /^[\w-]+(\.[\w-]+)*@[\w-]+(\.[\w-]+)+$/;    //邮箱的正则校验规则
    var qqRule = /^[1-9][0-9]{4,14}$/;  //QQ的正则校验规则

    //添加电话
    $('.add-phone-btn').click(function(){
        var htmls = $('#J-model-phone').html();
        $('.phone-list').append(htmls)
    });

    $('.phone-list').on('click', '.del-phone-btn',function(){
        $(this).closest(".basic-info-list").remove();
    });

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

    var uploader = $("#J-logo-FormFile");
    var uploader2 = $("#J-bg-FormFile");

    uploader.fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles : 1,
        maxFileSize: 5000000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('.logo-bg img').attr('src', file.url);
            });
        }
    });
    uploader.find("input:file").removeAttr('disabled');

    uploader2.fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles : 1,
        maxFileSize: 5000000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('.bg-img img').attr('src', file.url);
            });
        }
    });
    uploader2.find("input:file").removeAttr('disabled');

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
    }

    $('input[name="company_name"]').change(function(){
        var name = $(this).val().trim();
        name!="" ? $('.company-name-err').text("") : $('.company-name-err').text("装修公司名称不能为空！");
    });
    $('input[name="detail_address"]').change(function(){
        var address = $(this).val().trim();
        address!="" ? $('.detail-address-err').text("") : $('.detail-address-err').text("详细地址不能为空！");
    });
    $('input[name="contacts"]').change(function(){
        var contact = $(this).val().trim();
        contact!="" ? $('.contacts-err').text("") : $('.contacts-err').text("联系人不能为空！");
    });
    $('.phone-list').on('change', 'input[name="contacts_tel"]',function(){
        var phone = $(this).val().trim();
        if(phone==""){
            $(this).siblings('.contacts-tels-err').text("联系电话不能为空！")
        }else{
            if(mobileRule.test(phone)){
                $(this).siblings('.contacts-tels-err').text("");
            }else{
                $(this).siblings('.contacts-tels-err').text("联系电话格式不正确！")
            }
        }
    });
    $('input[name="mail"]').change(function(){
        var mail = $(this).val().trim();
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

    $('.basic-info-save-btn').click(function(){
        var name = $('input[name="company_name"]').val().trim();
        var province = $('.province').val();
        var city = $('.city').val();
        var area = $('.county').val();
        var address = $('input[name="detail_address"]').val().trim();
        var contact = $('input[name="contacts"]').val().trim();
        var phone = new Array();
        $('input[name="contacts_tel"]').each(function(){
            phone.push($(this).val());
        });
        var qq = $('input[name="qq"]').val().trim();
        var mail = $('input[name="mail"]').val().trim();
        var desc = $('.basic-info-textarea').val();
        var photo_url = $('.logo-bg img').attr("src");
        var background_url = $('.bg-img img').attr("src");
        var _xsrf = $('input[name="_xsrf"]').val();

        var result = true;     //全局保存判断

        if(name==""){
            result = false;
            alert("请填写装修公司名称...");
        }
        if(result){
            if(province=="" || province=="0"){
                result = false;
                alert("请选择省份！");
            }
            if(city=="" || city=="0"){
                result = false;
                alert("请选择市！");
            }
            if(area=="" || area=="0"){
                result = false;
                alert("请选择县，区！");
            }
        }
        if(result){
            if(address==""){
                result = false;
                alert("请填写详细地址！");
            }
        }
        if(result){
            if(contact==""){
                result = false;
                alert("请填写联系人！");
            }
        }
        if(result){
            for (i in phone) {
                if (phone[i] == "" || !mobileRule.test(phone[i])) {
                    result = false;
                    alert("联系电话为空或者格式不正确，请重新输入...");
                }
            }
        }
        if(result){
            if(qq!="" && !qqRule.test(qq)){
                result = false;
                alert("QQ格式不正确，如有需要，请重新输入...");
            }
        }
        if(result){
            if(mail=="" || !mailRule.test(mail)){
                result = false;
                alert("邮箱为空或者格式不正确，请重新输入...");
            }
        }
        if(result){
            var desc_length = desc.length;
            if(desc_length>300){
                result = false;
                alert("描述内容"+desc_length+"个字，请删减到300个字！");
            };
        }
        if(result){
            if(photo_url==""){
                result = false;
                alert("请上传logo！");
            }
        }
        if(result){
            if(background_url==""){
                result = false;
                alert("请上传一张背景图片！");
            }
        }
        if(result){
            var data_list = new Object();

            data_list.name = name;
            data_list.province = province;
            data_list.city = city;
            data_list.area = area;
            data_list.detail_address = address;
            data_list.contact = contact;
            data_list.phone = phone.join(',');
            data_list.qq = qq;
            data_list.mail = mail;
            data_list.desc = desc;
            data_list.photo_url = photo_url;
            data_list.background_url = background_url;
            data_list._xsrf = _xsrf;

            jQuery.ajax({
                type: "POST",
                url: "/merchant/company/edit",
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        location.href = "/merchants/index/" + data.id;
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