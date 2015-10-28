/**
 * Created by mele on 15/3/16.
 */
/**
 * Created by hujunhao on 15/1/29.
 */

var init = {
    loadPreComment: function(page,url){
        $('.comment-list').empty();

        var id = $('input[name="id"]').val();

        jQuery.ajax({
            type: "GET",
            url: url,
            data: {page:page},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    var list = data.list;
                    $.each(list, function(i){
                        var html = $('#J-model-comment').html();
                        var templates = toReplaceModel(html, list[i], "1");
                        $('.comment-list').append(templates);
                    });
                } else {
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    }
}
function toReplaceModel(html, list ,juage){
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{photo_url}}", list.photo);
    if(juage=="1"){
        html = html.replace("{{role}}", "");
    }else{
        html = html.replace("{{role}}", '<div class="diary-step-source small '+ list.user_codes +'"></div>');
    }
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{user_name}}", list.nick);
    html = html.replace("{{time}}", list.gmt_modified);
    html = html.replace("{{content}}", list.comment);

    return html;
}

$(document).ready(function(){

    $(".answer-he").click(function(e){
        e.preventDefault();
        var _this = $(this),
            parent = _this.closest(".answer-other"),
            input = parent.find(".answer-input");
        if (input.hasClass('hide')){input.removeClass('hide');}else{input.addClass('hide');}

    });

    $('.comment-content').focus(function(){
        if (!getCookie('loginuser')){
            $('#J-login').click();
        }
    });

    //提交评论
    $('.publish').click(function(){
        var _self = $(this);
        _self.attr("disabled", true);

        var id = $('input[name="id"]').val();
        var text = $('.comment-content').val();
        var _xsrf = $('input[name="_xsrf"]').val();
        var url = _self.attr("data-url");

        if(text!="") {
            jQuery.ajax({
                type: "POST",
                url: url,
                data: {text:text, _xsrf:_xsrf},
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        $('.comment-content').val("");
                        var list = data.list[0];
                        var html = $('#J-model-comment').html();
                        var templates = toReplaceModel(html, list, "1");
                        $('.comment-list').prepend(templates);
                    } else {
                        alert(data.msg);
                    }
                    _self.removeAttr("disabled");
                },
                error: function () {
                    _self.removeAttr("disabled");
                }
            });
        }else{
            _self.removeAttr("disabled");
        }
    });

    //各阶段评论唤起评论页面
    $('.answer-content-show').click(function(){
        $('input[name="list_id"]').attr("value", $(this).closest('.diary-list-item').attr("id"));
        $('input[name="list_data_id_main"]').attr("value", $(this).closest('.diary-list-item').attr("data-id-main"));
        //$('input[name="list_data_url"]').attr("value", $(this).attr("data-url"));
        var height = $(document).height();
        $('.comment-box').css("height", height).show();
        $('.answer-content').focus();
    });

    //各阶段提交评论
    $('.comment-btn').click(function(){
        var _self = $(this);
        _self.attr("disabled", true);

        mBase.isLogin();//登录校验

        var id = $('input[name="article_id"]').val();
        var text = $('.answer-content').val();
        var _xsrf = $('input[name="_xsrf"]').val();
        //var content_id = _self.closest(".diary-list-item").attr("data-id-main");
        var content_id = $('input[name="list_data_id_main"]').val();
        var url = $('input[name="list_data_url"]').val();

        if(text!="") {
            jQuery.ajax({
                type: "POST",
                url: url,
                data: {text:text, content_id:content_id, _xsrf:_xsrf},
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        $('.comment-box').hide();
                        $('.answer-content').val("");
                        var list = data.list[0];
                        var html = $('#J-model-comment2').html();
                        var templates = toReplaceModel(html, list, "2");
                        var nowCommentCount = parseInt($("#"+content_id).find('.d-comment-count').text().split("条回复")[0]);
                        if(nowCommentCount==0){
                            $("#"+content_id).find('.answer-content-part').append('<div class="user-icon d-up-arrow"></div><div class="answer-list">'+templates+'</div>');
                        }else{
                            $("#"+content_id).find('.answer-list').prepend(templates);
                        }
                        $('#'+content_id).find('.d-comment-count').text(nowCommentCount+1+"条回复");
                    } else {
                        alert(data.msg);
                    }
                    _self.removeAttr("disabled");
                },
                error: function () {
                    _self.removeAttr("disabled");
                }
            });
        }else{
            _self.removeAttr("disabled");
        }
    });

    $('.lookMoreAnswer').click(function() {
        var _self = $(this);

        var id = $('input[name="article_id"]').val();
        if(id == ''){
            return;
        }
        var content_id = _self.closest(".diary-list-item").attr("data-id-main");
        jQuery.ajax({
            type: "GET",
            url: "/comment/article/" + id + "/" + content_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    var list = data.list;
                    var html = $('#J-model-comment2').html();
                    $.each(list, function(i){
                        var templates = toReplaceModel(html, list[i], "2");
                        _self.closest(".answer-content-part").find(".answer-list").append(templates);
                    });
                    _self.remove();
                } else {
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    });
});

//登录校验
function getCookie() {
    function escape(s) {
        return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
    }
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape('check_loginuser') + '=([^;]*)'));
    return match ? match[1] : null;
}