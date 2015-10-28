/**
 * Created by mele on 15/4/1.
 */
var Base = {};
Base.isLogin = function(){
    function escape(s) {
        return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
    }
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape('check_loginuser') + '=([^;]*)'));
    match = match ? match[1] : null;
    if(!match){$("#J-login").click();return false;}
    return true;

};
Base.like = function(spot,cancel){
    var lickFunc;
    var c = this;
    $(".like").on("click",lickFunc = function(){
        //login
        if(c.isLogin()){
            var that = $(this);
            if(that.hasClass("un")){
                that.removeClass("un").text(that.text()-0+1);
                if(that.hasClass("photo"))return like("/assist/image/spot",that);
                like(spot,that);
            }else{
                that.addClass("un").text(that.text()-1);
                if(that.hasClass("photo"))return like("/assist/image/cancel",that);
                like(cancel,that);
            }
        }
    });
    function like(url,that){
        $.ajax({
            url: url,
            type: "post",
            dataType: "json",
            data: {id: that.data("id"),
                content_id: that.data("content"),
                album_id: that.data("album_id")?that.data("album_id"):0,
                like_type: that.data("type"),
                "_xsrf": $("input[name='_xsrf']").val()
            },
            beforeSend: function(){
                that.off("click");
            },
            success: function(response){
                if(response.stat == "ok"){
                    that.on("click",lickFunc);
                }
            }
        })
    }
};
//serialize
Base.serializeForm = function (o){
    if(o){
        o = o.serializeArray();
        var O = {};
        $.each(o,function(i){
            var oi = o[i];
            O[oi["name"]] = oi["value"];
        });
        return O;
    }
}

//$(function(){
//    //$('.yunriji').click(function(){
//    //    alert("此日记来自于怎么装“云端监理”系统，项目经理、监理、业主、全程互动直播，100%真实");
//    //})
//})



//页面滚动监听
window.onscroll = function(){
    var v_height = $(window).height();  //浏览器当前窗口可视区域高度
    var scroll = document.documentElement.scrollTop || document.body.scrollTop;
    parseInt(scroll) > parseInt(v_height) ? $('.back-to-top').show() :  $('.back-to-top').hide();
}

$(function(){
    //图片延迟加载
    $("img.gzh-lazy").lazyload({
        //effect : "fadeIn",
        placeholder :"/static/skin/js/plugins/lazyLoad/default.jpg",
        data_attribute: "lazyload",
        failure_limit : 10
    }) ;

    //个人中心导航显示与隐藏
    $(".gzh-header-nav").hover(function(){
        $(this).find(".gzh-nav").show();
        return false;
    },function(){
        $(this).find(".gzh-nav").hide();
    });

    //显示二级菜单
    $('#nav .nav-item').dropdown({
        dropdownEl:'.nav-dropdown',
        openedClass:'hover'
    });

    $(".gzh-container .img-link").on({
        mouseenter: function () {
            $(this).parent().find(".img-cover").fadeIn();
        },
        mouseleave: function () {
            $(this).parent().find(".img-cover").fadeOut();
        }
    });
})