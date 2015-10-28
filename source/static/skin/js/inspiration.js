/**
 * Created by mengnan on 15/1/12.
 */
var $page = $('input[name="page"]');
var page = 0;
var data = {
    "_xsrf": $('input[name="_xsrf"]').val(),
    "order": $(".sort-tabs a.active").attr("data-id")
};
var btn = $('.pre-more');
//ajaxLoad("/inspiration/"+page,"pobst",data,false);

//图片切换
$('.case-list').on('click','.thumb',function(){
    var src = $(this).attr("data-src");
    $(this).closest("li").find(".main-img img").attr("src", src);
});
//分类以及排序
tabS($(".sort-tabs"),"a",function(){
    data["current_house_type_id"]   = $("#c_house_style").find(".ins-info-active").attr("data-id");
    data["current_room_id"]         = $("#c_construction_mode").find(".ins-info-active").attr("data-id");
    data["current_design_style_id"] = $("#c_design_style").find(".ins-info-active").attr("data-id");
    data["order"]                   = $(".sort-tabs a.active").attr("data-id");
    ajaxLoad("/inspiration/"+0,"post",data,true);
});
function ajaxLoad(url,type,data,clear){
    $.ajax({
        type: type,
        url: url,
        data: data,
        dataType: "json",
        success: function(response){
            var o = {
                page: response.page,
                list: response.inspirations,
                has_more: response.has_more
            };
            initInspiration(response,clear);
            $page.val(o.page);
            btn.text("更多");
            o.has_more ? btn.show().addClass("finish") : $('.pre-more').hide().removeClass("finish");

        },
        error: function(error){
            console.log(error);
        }
    })
}
//加载更多
$(document).scroll(function(){
    if($(document).scrollTop() >= btn.offset().top - $(window).height() && btn.hasClass("finish")){
        btn.text("加载中...").removeClass("finish");
        ajaxLoad("/inspiration/"+(- - $page.val()+1),"post",data,false);
    }
});
function initInspiration(o,clear) {
    if(clear){
        $(".case-list").html("");
    }
    var room_id = o.current_room_id;
    var o = o.inspirations;
    var formater = "";
    var len= o.length;
    var count = 3;
    var int = parseInt(len/count);
    if(len){
        //判断是否是room类型
    if(room_id != "-1"){
        var column = $('.column');
        if(column.length){
            for(var i= 0;i<len;i=i+count){
                for(var j=0;j<count;j++){
                    var oi = o[i+j];
                    formater = '<div>' +
                    '<a href="' + '/merchants/product/detail/'+oi.product_id + '" class="main-img choice-case" target="_blank" >' +
                    '<img src="' + oi.url + '">' +
                        //'<span>'+'<em>'+oi.construction_mode_name +' | ￥'+ oi.total_price+'</em>'+oi.design_style_name+' | '+oi.area+' ㎡</span>'+
                    '</a>' +
                    '<p class="decription">' + '<a class="product" href="' + '/merchants/product/detail/'+oi.product_id + '" target="_blank" >'+ oi.title + '</a>   ' +
                    '来自<a class="company" href="' + '/merchants/index/'+ oi.user_id + '" target="_blank" >' + oi.name + '</a>' + '</p>' +
                    '</div>';
                    column.eq(j).append(formater);
                    //if(j == count-1){
                    //    i = i+count;
                    //}
               }
            }
        }else{
            for(var wrapI= 0;wrapI<count;wrapI++){
                formater += '<li class="column">';
                //大于列数
                if(len>=count){
                    for(var item= int*wrapI;item<int*(wrapI+1);item++){
                        var oi = o[item];
                        formater += '<div>' +
                        '<a href="' + '/merchants/product/detail/'+oi.product_id + '" class="main-img choice-case" target="_blank" >' +
                        '<img src="' + oi.url + '">' +
                            //'<span>'+'<em>'+oi.construction_mode_name +' | ￥'+ oi.total_price+'</em>'+oi.design_style_name+' | '+oi.area+' ㎡</span>'+
                        '</a>' +
                        '<p class="decription">' + '<a class="product" href="' + '/merchants/product/detail/'+oi.product_id + '" target="_blank" >'+ oi.title + '</a>   ' +
                        '来自<a class="company" href="' + '/merchants/index/'+ oi.user_id + '" target="_blank" >' + oi.name + '</a>' + '</p>' +
                        '</div>';
                    }
                }else{
                    //小于列数
                    var oi = o[wrapI];
                    if(!oi){break;}
                    formater += '<div>' +
                    '<a href="' + '/merchants/product/detail/'+oi.product_id + '" class="main-img choice-case" target="_blank" >' +
                    '<img src="' + oi.url + '">' +
                        //'<span>'+'<em>'+oi.construction_mode_name +' | ￥'+ oi.total_price+'</em>'+oi.design_style_name+' | '+oi.area+' ㎡</span>'+
                    '</a>' +
                    '<p class="decription">' + '<a class="product" href="' + '/merchants/product/detail/'+oi.product_id + '" target="_blank" >'+ oi.title + '</a>   ' +
                    '来自<a class="company" href="' + '/merchants/index/'+ oi.user_id + '" target="_blank" >' + oi.name + '</a>' + '</p>' +
                    '</div>';
                }

                formater += '</li>';
            }
            $(".case-list").append(formater);
        }
    }else{
        $.each(o, function (i) {
            var oi = o[i];
            formater += '<li>' +
            '<a href="' + '/merchants/product/detail/'+oi.product_id + '" class="main-img choice-case" target="_blank" >' +
            '<img src="' + oi.show_main_url + '" title="' + oi.product_desc + '" alt="' + oi.product_desc + '">' +
            '<span>'+'<em>'+oi.construction_mode_name +' | ￥'+ oi.total_price+'</em>'+oi.design_style_name+' | '+oi.area+' ㎡</span>'+
            '</a>' +
            '<div class="thumb-part clearfix">' +
            '<img src="' + oi.show_url + '" data-src ="' + oi.show_main_url + '" class="thumb" alt="">' +
            '<img src="' + oi.show_url1 + '" data-src ="' + oi.show_main_url1 + '" class="thumb" alt="">' +
            '<img src="' + oi.show_url2 + '" data-src ="' + oi.show_main_url2 + '" class="thumb" alt="">' +
            '</div>' +
            '<div class="case-info">' +
            '<a class="merchant-link" href="' + '/merchants/index/' + oi.company_user_id + '" target="_blank" ><img src="' + oi.photo_url + '" alt=""/></a>' +
            '<div class="case-info-txt">' +
            '<p class="case-name"><a href="' + '/merchants/product/detail/'+oi.product_id + '" target="_blank" >' + oi.title + '</a></p>' +
            '<p class="company">来自<a href="' + '/merchants/index/'+ oi.company_user_id + '" target="_blank" >' + oi.name + '</a></p>' +
            '</div>' +
            '</div>' +
            '</li>';
        });
        $(".case-list").append(formater);
        }
    }



    //瀑布流取余
    if(item&&len%count){
        for(var i=0;i<len%count;i++){
            oi = o[item+i];
            var html = '<div>' +
                '<a href="' + '/merchants/product/detail/'+oi.product_id + '" class="main-img choice-case" target="_blank" >' +
                '<img src="' + oi.url + '">' +
                    //'<span>'+'<em>'+oi.construction_mode_name +' | ￥'+ oi.total_price+'</em>'+oi.design_style_name+' | '+oi.area+' ㎡</span>'+
                '</a>' +
                '<p class="decription" title="'+oi.description+'">'+oi.description+'</p>'+
                '</div>';
            $(".column:eq("+i+")").append(html);
        }
    }
}
//灵感信息选择条件操作
$('.select-things').click(function(){
    var _self = $(this);
    if(!_self.hasClass("ins-info-active")){
        _self.closest(".ins-info-select").find(".select-things").each(function (){
            $(this).hasClass("ins-info-active") ? $(this).removeClass("ins-info-active") : "";
        });
        _self.addClass("ins-info-active");
        data["current_house_type_id"] = $("#c_house_style").find(".ins-info-active").attr("data-id");
        data["current_room_id"] = $("#c_construction_mode").find(".ins-info-active").attr("data-id");
        data["current_design_style_id"] = $("#c_design_style").find(".ins-info-active").attr("data-id");
        //var order_sort =
        data["order"] = $(".sort-tabs a.active").attr("data-id");
        ajaxLoad("/inspiration/"+0,"post",data,true);
        //page = 0;
        //data[""]
    }
});
//tabSelect
function tabS(o,tagName,func){
    var sub = o.find(tagName);
    sub.click(function(){
        var _self = $(this);
        if(!_self.hasClass("active")){
            sub.each(function(i){
                sub.eq(i).hasClass("active") ? sub.eq(i).removeClass("active") : "";
            });
        }
        _self.addClass("active");
        func();
    })
}