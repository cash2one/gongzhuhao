/**
 * Created by hujunhao on 15/1/7.
 */
var init = {
    comment: function(page_size, id){
        var line = '<li class="cut-line"></li>';

        jQuery.ajax({
            type: "GET",
            url: '/comment/shopping_list/'+id,
            data: {page_size:page_size},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(stat=="ok") {
                    var list = data.list;

                    $.each(list, function(i){
                        var html = $('#J-model-first-comment').html();
                        var templates = toReplaceModel(html, list[i]);
                        $('.first-comment').append(($('.first-comment li').length>0 ? line : "") + templates);

                        var reply_list = list[i].reply_list;
                        if(reply_list.length>0) {
                            $.each(reply_list, function (k) {
                                var html = $('#J-model-second-comment').html();
                                var templates = toReplaceModel(html, reply_list[k]);

                                var s = $('li[data-id="' + list[i].id + '"]');
                                s.find('.son-comment-box').css("display", "block");
                                s.find('.second-comment').append((s.find('.second-comment li').length > 0 ? line : "") + templates);
                            });
                        }
                    });
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    }

}

/* 模板加载需先加载空模板 */
function toReplaceModel(html, list){
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{nick}}", list.nick);
    html = html.replace("{{photo}}", list.photo);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{nick}}", list.nick);
    html = html.replace("{{nick}}", list.nick);
    html = html.replace("{{comment}}", list.comment);
    html = html.replace("{{gmt_modified}}", list.gmt_modified);

    return html;
}

$(document).ready(function() {

    //毕业照--upload上传图片
    $('#fileupload').click(function () {
        var uploader = $("#J-formFile");
        var i = $('#J-append-photo li').length;
        addPhoto(uploader, i);
    });

    //用户主页上传毕业照
    function addPhoto(uploader, i) {
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            //maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('#J-append-photo li:eq(' + i + ')').attr("data-id", file.id);
                    $('#J-append-photo li:eq(' + i + ')').find("img").attr("src", file.url);
                    i++;
                });
            },
            send: function (e, data) {
                var html = $('#J-model-photo').html();
                $('#J-append-photo').append(html);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    }

    //装修日记--upload上传图片
    $('#fileupload-diary').click(function () {
        var uploader = $("#J-diary-formFile");
        var i = $('.diary-photo-list li').length;
        addDiaryPhoto(uploader, i);
    });

    //用户主页上传装修日记照片
    function addDiaryPhoto(uploader, i) {
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            //maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('.diary-photo-list li:eq(' + i + ')').attr("data-id", file.id);
                    $('.diary-photo-list li:eq(' + i + ')').find("img").attr("src", file.url);
                    i++;
                });
            },
            send: function (e, data) {
                var html = $('#J-model-diary-photo').html();
                $('.diary-photo-list').append(html);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    }
    //autoComplete
    autoComplete($("#c_community"),"/member/decorate_base/community/get",function(data,i){return '<p class="c-list" data-id="'+data[i].id+'">'+data[i].name+'</p>';});//小区
    autoComplete($('#c_company'),"/member/decorate_base/company_name/get",function(data,i){return '<p class="c-list" data-id="'+data[i].id+'">'+data[i].company+'</p>';});//装修公司
    /* 标题信息保存 */
    $('#J-themeName').blur(function () {
        var _self = $(this);
        var title = _self.val().trim();

        if (title == "") {
            alert("请输入标题！");
            _self.focus();
        }else{
            saveHeadInfo();
        }
    });
    $('.theme-name-show').click(function () {
        $(this).hide();
        $('#J-themeName').show().focus();
    });

    /* 户型、风格、施工方式的选择保存 */
    $('.select-things').click(function(){
        var _self = $(this);

        if(!_self.hasClass("create-head-active")){
            _self.closest(".create-head-info-select").find(".select-things").each(function (){
                $(this).hasClass("create-head-active") ? $(this).removeClass("create-head-active") : "";
            });
            _self.addClass("create-head-active");
            saveHeadInfo();
        }
    });

    /*  面积、小区、装修公司的数据保存 */
    $('.input-things').blur(function(){
        saveHeadInfo();
    });

    //保存信息
    function saveHeadInfo(){
        var title = "",
            house_type = "",
            design_style = "",
            m2 = "",
            construction_mode = "",
            community_name = "",
            community_id = "",
            company_name = "",
            company_id = "",
            _xsrf = $('input[name="_xsrf"]').val();

        /* 标题 */
        title = $('#J-themeName').val();

        /* 户型 */
        $('#c_house_style .select-things').each(function(){
            $(this).hasClass("create-head-active") ? house_type = $(this).attr("data-id") : "";
        });

        /* 风格 */
        $('#c_design_style .select-things').each(function(){
            $(this).hasClass("create-head-active") ? design_style = $(this).attr("data-id") : "";
        });

        /* 面积 */
        m2 = $('#c_area').val();

        /* 施工方式 */
        $('#c_construction_mode .select-things').each(function(){
            $(this).hasClass("create-head-active") ? construction_mode = $(this).attr("data-id") : "";
        });

        /* 小区 */
        community_name = $('#c_community').val();
        community_id = $("#c_community").attr("data-id");

        /* 装修公司 */
        company_name = $('#c_company').val();
        company_id = $('#c_company').attr("data-id");

        var data_list = new Object();

        data_list.title = title;
        data_list.house_type = house_type;
        data_list.design_style = design_style;
        data_list.m2 = m2;
        data_list.construction_mode = construction_mode;
        data_list.community_name = community_name;
        data_list.community_id = community_id;
        data_list.company_name = company_name;
        data_list.company_id = company_id;
        data_list._xsrf = _xsrf;

        jQuery.ajax({
            type: "POST",
            url: "/member/decorate_base/update",
            data: data_list,
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    $('#J-themeName').hide();
                    $('.theme-name-show').text(title).show();
                }
            },
            error: function () {
            }
        });
    }

    /* 照片描述保存操作 */
    $('.create-main-right').on('change', '.upload-photo-select', function(){
        $(this).closest(".photo-list-id").find(".upload-opcity-btn").show();
    });
    $('.create-main-right').on('input propertychange', '.upload_photo_desc', function() {
        $(this).closest(".photo-list-id").find(".upload-opcity-btn").show();
    });
    $('.create-main-right').on('click', '.upload-photo-cancel', function(){
        $(this).closest(".upload-opcity-btn").hide();
    });

    $('.create-main-right').on('click', '.upload-photo-save', function(){
        var _self = $(this);
        var id = _self.closest(".photo-list-id").attr("data-id"),
            type = _self.closest(".photo-list-id").find(".upload-photo-select").val(),
            desc = _self.closest(".photo-list-id").find(".upload_photo_desc").val(),
            _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/member/photo/edit/",
            data: {id:id, type:type, desc:desc, _xsrf:_xsrf},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    _self.closest(".upload-opcity-btn").hide();
                }
            },
            error: function () {
            }
        });
    });

    //装修日记上传图片，鼠标移上显示删除按钮
    $(".diary-photo-list").on('mouseover', ".d-p-list", function(event) {
        $(this).closest('.d-p-list').find('.diary-photo-close').show();
    }).on('mouseout', ".d-p-list", function(event) {
        $(this).closest('.d-p-list').find('.diary-photo-close').hide();
    });

    //装修日记上传图片删除
    $('.diary-photo-list').on('click', ".diary-photo-close", function(){
        var _self = $(this);
        var id = $(this).closest("li").attr("data-id"),
            _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/member/decorate_article_pic/delete",
            data: {id:id, _xsrf:_xsrf},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    _self.closest("li").remove();
                }
            },
            error: function () {
            }
        });
    });

    //装修日记信息保存
    $('.user-diary-save-btn').click(function(){
        var stage_id = $('.diary-step-select').val();
        var title = $('#J-themeName').val();

        var dp_list = $('.diary-photo-list li');
        if (dp_list.length != 0) {
            var diary_photo = new Array();
            dp_list.each(function (i) {
                var list = new Object();
                list.id = $(this).attr("data-id");
                list.src = $(this).find("img").attr("src");
                list.diary_photo_desc = $(this).find("input[name='diary_photo_desc']").val();

                diary_photo[i] = list;
            });
        }

        var desc = $('#J_diary_desc').val();
        var startDate = $('#startDate').val();
        var _xsrf = $('input[name="_xsrf"]').val();
        var type = $('#type').val();
        var id = $('#id').val();

        /* 标题 */
        if(title=="") {
            alert("请输入标题！");
            $('#J-themeName').focus();
            return;
        }

        /* 户型 */
        var house_type = '';
        $('#c_house_style .select-things').each(function(){
            $(this).hasClass("create-head-active") ? house_type = $(this).attr("data-id") : "";
        });
        if(house_type == ''){
            alert('请选择户型！');
            return;
        }

        /* 风格 */
        var design_style = '';
        $('#c_design_style .select-things').each(function(){
            $(this).hasClass("create-head-active") ? design_style = $(this).attr("data-id") : "";
        });
        if(design_style == ''){
            alert('请选择风格！');
            return;
        }

        /* 面积 */
        var m2 = $('#c_area').val();
        if(isNaN(m2)){
            alert('面积请输入数值！');
            return;
        }
        m2 = parseFloat(m2);
        if(m2 == 0.0){
            alert('请输入面积！');
            return;
        }


        /* 施工方式 */
        var construction_mode = '';
        $('#c_construction_mode .select-things').each(function(){
            $(this).hasClass("create-head-active") ? construction_mode = $(this).attr("data-id") : "";
        });
        if(construction_mode == ''){
            alert('请选择施工方式！');
            return;
        }

        if (stage_id == "-1") {
            alert("请选择装修阶段！");
        }

        /* 装修时间 */
        if(startDate == ''){
            alert('请选择装修时间！');
            return;
        }

        /* 日记描述图片没有的时候，文字描述必须要有，并且要大于10个字 */
        if(dp_list.length==0){
            if(desc=="" || desc.length<10){
                alert('请输入日记描述，并大于10个字！');
                return;
            }
        }

        if (stage_id != "-1") {

            var data_list = new Object();

            data_list.stage_id = stage_id;
            data_list.cdate = startDate;
            data_list.img_list = JSON.stringify(diary_photo);
            data_list.desc = desc;
            data_list.type = type;
            data_list.id = id;
            data_list._xsrf = _xsrf;

            jQuery.ajax({
                type: "POST",
                url: "/member/decorate_article/edit",
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        alert("保存成功！");
                        $('.diary-step-select').val(-1);
                        $('.diary-photo-list').empty();
                        $('#J_diary_desc').val("");
                        $('#type').val('new');
                        window.location.reload();
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        } else {
            alert("请选择装修阶段！");
        }
    });

    //采购清单展示盒隐藏部分
    $('.first-show').click(function(){
        $(this).closest("li").find(".detail-shopping-list").slideToggle("slow");
    });

    //毕业照描述信息保存
    $('#desc_save').click(function(){
        var desc = $('#img_desc').val(),
            _xsrf = $('input[name="_xsrf"]').val(),
            title = $('#J-themeName').val();

        if(title!="") {
            jQuery.ajax({
                type: "POST",
                url: "/album/byz/edit",
                data: {desc:desc, _xsrf:_xsrf},
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        alert("保存成功！");
                    }else{
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        }else{
            alert("请输入标题！");
            $('#J-themeName').focus();
        }
    });

    //毕业照设为封面和删除按钮的显示和隐藏
    $(".photo-img-show").on('mouseover', ".photo-list-id", function(event) {
        $(this).find('.set-face').show();
        $(this).find('.upload-photo-close').show();
    }).on('mouseout', ".photo-list-id", function(event) {
        $(this).find('.set-face').hide();
        $(this).find('.upload-photo-close').hide();
    });

    //毕业照设为封面
    $('.photo-img-show').on('click', '.set-face', function(){
        var id = $(this).closest(".photo-list-id").attr("data-id"),
            url = "/album/photo/set_cover/",
            type = "set_face";

        photoDeal(id, url, type);
    });

    //毕业照删除
    $('.photo-img-show').on('click', '.upload-photo-close', function(){
        var id = $(this).closest(".photo-list-id").attr("data-id"),
            url = "/album/photo/delete/",
            type = "delete_photo";

        photoDeal(id, url, type);
    });

    function photoDeal(id, url, type){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: url,
            data: {id:id, _xsrf:_xsrf},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(type=="set_face"){
                    stat=="ok" ? alert("设置成功！") : alert("设置失败！");
                }else if(type=="delete_photo"){
                    stat=="ok" ? window.location.reload() : alert("删除毕业照失败！");
                }
            },
            error: function () {
            }
        });
    }

    //采购清单继续操作出现二级类目list
    $('.to-add').mouseover(function(event){
        event.stopPropagation();
        var _self = $(this);

        //所有二级类目浮层全部隐藏掉
        $(".second-type-show").hide();

        var id = _self.closest(".first-show").find(".total-name").attr("data-id");
        var listNo = "";
        _self.closest(".first-show").find(".category").empty();

        var list = shopping_list.list;
        $.each(list, function(i){
            (list[i].id==id) ? listNo=i : "";
        });

        var second = list[listNo].category;
        $.each(second, function(i){
            var category = '<a href="javascript:void(0)" data-id="'+ second[i].id +'" class="second-category">'+ second[i].name +'</a>';
            _self.closest(".first-show").find(".category").append(category);
        });

        _self.closest(".first-show").find(".second-type-show").show();
    });

    //装修日记阶段切换，数据显示
    $('.diary-step-select').change(function(){
    //    var id = $(this).val();
    //    id!=-1 ? changeDiaryStepData(id) : "";

          $('#id').val('-1');
          $('#type').val('new');
          $('.diary-photo-list').empty();
          $('#J_diary_desc').val("");
    });

    //装修日记删除
    $('.diary-delete').click(function(){
        var id_main = $(this).closest("li").attr("data-id-main");
        window.location = "/member/decorate_article/delete/" +  id_main;
    });

    //装修日记修改
    $('.diary-modify').click(function(){
        var id = $(this).closest("li").attr("data-id");
        $('.diary-step-select').val(id);

        var id_main = $(this).closest("li").attr("data-id-main");
        $('#id').val(id_main);
        $('#type').val('modify');
        $('.diary-photo-list').empty();
        $('#J_diary_desc').val("");

        changeDiaryStepData(id_main);
    });

    //装修日记数据切换显示
    function changeDiaryStepData(id){
        var close = '<a href="javascript:void(0)" class="user-icon diary-photo-close" style="display: none;"></a>';

        jQuery.ajax({
            type: "GET",
            url: "/member/decorate_article/get/"+id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(stat=="ok"){
                    $('.diary-photo-list').empty();
                    $('#J_diary_desc').val(data.desc);

                    var images = data.images;

                    $.each(images, function(i){
                        var img = '<img src="'+ images[i].url +'" alt="" class="d-p-img">';
                        var desc = '<input type="text" name="diary_photo_desc" value="'+ images[i].desc +'" placeholder="描述(最多50字)" maxlength="50">';
                        var li = '<li data-id="'+ images[i].id +'" class="d-p-list">'+ close + img + desc +'</li>';
                        $('.diary-photo-list').append(li);
                    });
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    }

    //二级类目浮层显示,新建
    $('.shopping-list').on('click', '.second-category', function(){
        var category_1 = $(this).closest(".first-show").find(".total-name").attr("data-id");
        var category_2 = $(this).attr("data-id");

        addCategory(category_1, category_2);

        category_2 == "0" ? $('.hidename').show() : $('.hidename').hide();
        $('.add-shop-list-input').val("");
        $('.shopping_recommend')[0].selectedIndex = 0;
        $('.shopping_remark').val("");
        $('.sp-btn').attr("data-url", "/member/shopping_list/create");
        $('#shoppingListModal').modal();
    });

    //加载浮层一、二级类目
    function addCategory(category_1, category_2){
        var listNo = "";
        $('.layer-first-category').empty();

        //类目一加载匹配
        var list = shopping_list.list;
        $.each(list, function(i){
            $('.layer-first-category').append('<option value="'+ list[i].id +'">'+ list[i].name +'</option>');
            (list[i].id == category_1) ? listNo = i : "";
        });
        $(".layer-first-category").val(category_1);

        //类目二加载匹配
        var second = list[listNo].category;
        $(".layer-second-category").empty();

        $.each(second, function(k){
            $('.layer-second-category').append('<option value="'+ second[k].id +'">'+ second[k].name +'</option>');
        });
        $(".layer-second-category").val(category_2);
    }

    //采购清单浮层类目二级联动
    $(".layer-first-category").change(function(){
        $(".layer-second-category").empty();

        var id = $(this).val(), list = shopping_list.list, listNo = "";
        $.each(list, function(i){
            list[i].id == id ? listNo = i : "";
        });

        var second = list[listNo].category;
        $.each(second, function(k){
            $('.layer-second-category').append('<option value="'+ second[k].id +'">'+ second[k].name +'</option>');
        });
        $('.layer-second-category')[0].selectedIndex = 0;
    });

    $(".layer-second-category").change(function(){
        $(this).val() == "0" ? $('.hidename').show() : $('.hidename').hide();
    });

    //编辑修改采购清单
    $('.sp-modify').click(function(){
        var category_1 = $(this).closest("li").find(".total-name").attr("data-id");
        var category_2 = $(this).closest(".shopping-record").attr("data-category");
        var id = $(this).closest(".shopping-record").attr("data-id");
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/member/shopping_list/get",
            data: {list_id:id, _xsrf:_xsrf},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok"){
                    var list = data.list;
                    $('input[name="shopping_name"]').val(list.name);  //(品牌/公司)名称
                    $('input[name="shopping_brand"]').val(list.brand);    //品牌
                    $('input[name="shopping_place"]').val(list.shopping_place); //购买地址
                    $('input[name="shopping_total_price"]').val(list.total_price);   //总价
                    $('input[name="shopping_total_count"]').val(list.total_count);   //数量
                    $('.shopping_recommend').val(list.recommend);     //是否值得推荐
                    $('.shopping_remark').val(list.remark);    //备注

                    addCategory(category_1, category_2);
                    category_2 == "0" ? $('.hidename').show() : $('.hidename').hide();

                    $('.sp-btn').attr("data-url", "/member/shopping_list/edit");
                    $('.sp-btn').attr("data-listId", id);

                    $('#shoppingListModal').modal();
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    });

    //删除采购清单数据
    $('.sp-delete').click(function(){
        var _self = $(this);
        var id = $(this).closest(".shopping-record").attr("data-id"),
            _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/member/shopping_list/delete",
            data: {list_id:id, _xsrf:_xsrf},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok"){
                    _self.closest(".shopping-record").remove();
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    });

    //新建，编辑采购清单提交
    $('.sp-btn').click(function(){
        var result = true;
        $('.result_err').empty();
        var url = $(this).attr("data-url"),
            id = $(this).attr("data-listId");

        var material_first_id = $('.layer-first-category').val(),   //建材类型一级分类id
            material_second_id = $('.layer-second-category').val(),    //建材类型二级分类id
            name = $('input[name="shopping_name"]').val(),  //(品牌/公司)名称
            brand = $('input[name="shopping_brand"]').val(),    //品牌
            shopping_place = $('input[name="shopping_place"]').val(), //购买地址
            total_price = $('input[name="shopping_total_price"]').val(),   //总价
            total_count = $('input[name="shopping_total_count"]').val(),   //数量
            recommend = $('.shopping_recommend').val(),     //是否值得推荐
            remark = $('.shopping_remark').val(),    //备注
            _xsrf = $('input[name="_xsrf"]').val();

        //二级类目为其他时，显示自由输入内容，否则就显示二级类目的内容
        var material_second_name = $('.layer-second-category').find("option:selected").text();    //建材类型二级分类name
        material_second_id != "0" ? name = material_second_name : "";

        //总金额校验
        var patrn=/^(-)?(([1-9]{1}\d*)|([0]{1}))(\.(\d){1,2})?$/;
        if(!patrn.test(total_price)){
            $('.price_err').text("金额输入有误，请重输...");
            result = false;
        }else{
            $('.price_err').empty();
        }

        //数量校验
        var number_rule = /^\+?[1-9][0-9]*$/;
        if(total_count.trim()!="" && !number_rule.test(total_count)){
            $('.count_err').text("数量格式输入有误，请重输...");
            result = false;
        }else{
            $('.count_err').empty();
        }

        if(result) {
            var data_list = new Object();

            data_list.material_first_id = material_first_id;
            data_list.material_second_id = material_second_id;
            data_list.name = name;
            data_list.brand = brand;
            data_list.shopping_place = shopping_place;
            data_list.total_price = total_price;
            data_list.total_count = total_count;
            data_list.recommend = recommend;
            data_list.remark = remark;
            data_list._xsrf = _xsrf;
            data_list.list_id = id;

            jQuery.ajax({
                type: "POST",
                url: url,
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    data.stat == "ok" ? window.location.reload() : $('.result_err').text(data.msg);
                },
                error: function () {
                }
            });
        }
    });




    ////个人主页装修公司实时搜索
    //$('#c_company').on('input propertychange', function() {
    //    var _self = $(this).closest("li").find(".companyResult");
    //    $(this).attr("data-id", "");
    //    var name = $(this).val();
    //
    //    if(name==""){
    //        _self.empty().hide();
    //    }else{
    //        jQuery.ajax({
    //            type: "POST",
    //            url: "/member/decorate_base/company_name/get",
    //            data: {'name':name,'_xsrf':$('input[name="_xsrf"]').val()},
    //            dataType: "JSON",
    //            success: function (data) {
    //                _self.empty();
    //
    //                if(data.length>0) {
    //                    $.each(data, function(i){
    //                        var p = '<p class="c-list" data-id="'+data[i].id+'">'+data[i].company+'</p>';
    //                        _self.append(p);
    //                    });
    //                    _self.show();
    //                }
    //            },
    //            error: function () {
    //            }
    //        });
    //    }
    //});
    //$('.companyResult').on("click", ".c-list", function(){
    //    var _self = $(this);
    //    var name = _self.text(),
    //        id = _self.attr("data-id");
    //    _self.closest("li").find("#c_company").val(name).attr("data-id", id).focus();
    //    $('.companyResult').empty().hide();
    //
    //});

    function autoComplete (o,url,htmlFunc){
        var hidden = o.nextAll("input[type='hidden']").eq(0);
        //result
        var result = o.after('<div class="companyResult" style=""></div>').next();
        //event
        o.on("input propertychange",function(){
            var that = $(this), val = that.val();
            that.attr("data-id","");
            hidden.val("");
            if (val == "") {
                //clear
                result.empty().hide();
            } else {
                $.post(url,{"name":val,"_xsrf":$('input[name="_xsrf"]').val()},function(data){
                    //clear
                    result.empty();
                    $.each(data, function(i){
                        result.append(htmlFunc(data,i));
                    });
                    result.show();
                },"json")
            }
        });
        result.on("click",".c-list",function(){
            var that = $(this);
            var name = that.text(),
                id = that.data("id");
            o.val(name).attr("data-id", id).focus();
            hidden.val(id);
            result.empty().hide();
        });
    }

    //登录校验
    function getCookie() {
        function escape(s) {
            return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
        }
        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape('check_loginuser') + '=([^;]*)'));
        return match ? match[1] : null;
    }

    $('.comment').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.replay').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.first-comment').on('click', '.comment-answer', function(){
        var l = $(this).closest('li'),
            step = $(this).attr("data-step");
        var user_name = l.find('.user-name').eq(0).text();

        step=="1" ? l.find('.son-comment-box').slideToggle() : "";
        l.find('.replay').attr("placeholder", "回复 " + user_name + ":");
    });

    $('.send').click(function(){
        if (!getCookie()){
            $('#J-login').click();
        }else{
            var data = new Object();
            data.text = $('.comment').val();
            data._xsrf = $('input[name="_xsrf"]').val();

            var step = $(this).attr("data-step");
            commentAdd(data, step);
        }
    });
    $('.first-comment').on('click', '.replay-btn', function(){
        if (!getCookie()){
            $('#J-login').click();
        }else{
            var data = new Object();
            var _self = $(this);

            data.text = _self.closest('.replay-part').find('.replay').val();
            data.user_id = _self.closest('li').attr("data-userid");
            data.p_id = _self.closest('li').attr("data-id");
            data._xsrf = $('input[name="_xsrf"]').val();

            var step = $(this).attr("data-step");
            commentAdd(data, step);
        }
    });

    function commentAdd(data, step){
        var id = $('input[name="user"]').val(),
            line = '<li class="cut-line"></li>',
            li_id = data.p_id;

        jQuery.ajax({
            type: "POST",
            url: '/comment/shopping_list/'+id,
            data: data,
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(stat=="ok") {
                    var list = data.list;

                    if(step=="3"){
                        $('.comment').val("");
                        var html = $('#J-model-first-comment').html();
                        var templates = toReplaceModel(html, list[0]);

                        $('.first-comment').prepend(templates + ($('.first-comment li').length>0 ? line : ""));
                    }else if(step=="4"){
                        $('.replay').val("");
                        var html = $('#J-model-second-comment').html();
                        var templates = toReplaceModel(html, list[0]);

                        var s = $('li[data-id="'+li_id+'"]').find('.second-comment li');
                        $('li[data-id="'+li_id+'"]').find('.second-comment').prepend(templates + (s.length>0 ? line : ""));
                    }
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    }
});

