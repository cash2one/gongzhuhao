/**
 * Created by yijiaren-sun on 14-12-22.
 */

var init = {
    loadComment: function(page){
        var url = '/guide/reply/' + $('input[name = "data_id"]').val();

        $.ajax({
            type: 'GET',
            url: url,
            data: {page: page},
            dataType: 'JSON',
            success: function (data) {
                if(data.stat == 'ok'){
                    var list = data.list;

                    $.each(list, function(i){
                        var html = $('#J-model-tip-comment').html();
                        var templates = toReplaceModel(html, list[i]);

                        $('.comment-list').append(templates);
                    });
                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        })
    }
}

/* 模板加载需先加载空模板 */
function toReplaceModel(html, list){
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{photo_url}}", list.photo_url);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{user_name}}", list.user_name);
    html = html.replace("{{time}}", list.time);
    html = html.replace("{{content}}", list.content);

    return html;
}

$(document).ready(function() {

    //登录校验
    function getCookie() {
        function escape(s) {
            return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
        }

        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape("check_loginuser") + '=([^;]*)'));
        return match ? match[1] : null;
    }

    //回复状态的切换
    $('.comment-flag').click(function () {
        if (!$(this).hasClass("comment-active")) {
            $('.comment-flag').removeClass("comment-active");
            $(this).addClass("comment-active");

            $(this).attr("data-flag") == "1" ? $('.comment-list').slideDown() : $('.comment-list').slideUp();
        }
    });

    $('.comment-content').focus(function () {
        if (!getCookie()) {
            $('#J-login').click();
        }
    });

    //提交评论
    $('.publish').click(function () {
        var error_flag = $(".comment-active").attr("data-flag");
        var text = $('.comment-content').val();
        var _xsrf = $('input[name="_xsrf"]').val();

        if (text != "") {
            var data_list = new Object();

            data_list.error_flag = error_flag;
            data_list.text = text;
            data_list._xsrf = _xsrf;

            $.ajax({
                type: 'POST',
                url: window.location.href,
                data: data_list,
                dataType: 'JSON',
                success: function (data) {
                    if (data.stat == 'ok') {
                        var list = data.list;

                        $('.comment-content').val("");
                        var html = $('#J-model-tip-comment').html();
                        var templates = toReplaceModel(html, list[0]);

                        $('.comment-list').prepend(templates);
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        } else {
            alert("评论内容不能为空！");
        }
    });

    //预览
    $('.view').click(function(){
        var width = $(window).width(),  //浏览器当前窗口可视区域宽度
            v_height = $(window).height(),  //浏览器当前窗口可视区域高度
            d_height = $(document).height();  //浏览器当前窗口文档的高度

        //黑色半透明遮罩层显示
        $('body').append('<div class="cover"></div>');
        $('.cover').css({"width": width, "height":d_height}).show();

        var modal_heigth = $('#tipViewModal').height();
        if(parseInt(modal_heigth)>=parseInt(v_height)){
            var top = 0;
        }else{
            var top = (parseInt(v_height)-parseInt(modal_heigth))/2;
        }
        var left = (parseInt(width)-780)/2;
        $('#tipViewModal').css({"left":left, "max-height":v_height, "top":top}).slideDown();

        if(parseInt($('.tip-modal-bode').height()) > parseInt(v_height)) {
            $('.tip-modal-bode').css({"max-height": v_height - 46, "overflow-y": "scroll"});
        }
    });

    $('.close').click(function(){
        $('#tipViewModal').slideUp();
        $('.cover').hide();
    });
});