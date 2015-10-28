/**
 * Created by hujunhao on 15/5/6.
 */

var topic = function(options){
    this.options = options;
    this.topic = $('.topicType');
    this.title = $('input[name="title"]');
    this.content = $('.topic-desc-content');
    this.page = $('input[name="page"]').val();
    this.total_page = $('input[name="total_page"]').val();
    this.err = $(".err");
}

topic.prototype = {
    init: function(){
        var that = this;
        parseInt(that.total_page) > 1 ? that.loadPage(that.page, that.total_page) : $('#J-manage-page').empty();
        var list = $('#topic li .topic-content'), detail = $('.topic-detail-content');

        var emotion = '';

        if(list.length>0)
            var emotion = list;
        if(detail.length>0)
            var emotion = detail;

        if(emotion!="") {
            emotion.each(function () {
                var content = $(this).html();
                content = that.replace_em_init(content);
                $(this).html(content);
            });
        }

        that.bindEvents();
    },
    bindEvents: function(){
        var that = this;

        //上传图片
        $('#fileupload_topic').click(function(){
            var uploader = $("#J-topic-formFile");
            var i = $('.upload-descImg-list li').length;
            that.addPhotos(uploader, i);
        });

        $('.topicType').focus(function(){
            if (!getCookie()) $('#J-login').click();
        });

        $('.topicTitle').focus(function(){
            if (!getCookie()) $('#J-login').click();
        });

        $('.topic-desc-content').focus(function(){
            if (!getCookie()) $('#J-login').click();
        });

        //提交话题
        $(".publishBtn").click(function(){
            if (!getCookie()){
                $('#J-login').click();
            }else {
                var _self = $(this);
                _self.attr("disabled", true);

                var topic = that.topic.val(),
                    title = that.title.val().replace(/\s+/g,""),
                    content = that.content.val(),
                    content = that.replace_em(content),
                    img = $('.upload-descImg-list li'),
                    result = true;

                //话题校验
                if (topic == '-1') {
                    that.topic.focus();
                    that.err.text("请选择话题！");
                    result = false;
                }

                //标题校验
                if (result) {
                    if (title.length < 2) {
                        that.title.focus();
                        that.err.text("请输入标题, 2-25个字！");
                        result = false;
                    }
                }

                //话题内容校验
                if (result) {
                    if (content.length < 5) {
                        that.content.focus();
                        that.err.text("请输入话题内容, 最少5个字！");
                        result = false;
                    }
                }

                //描述图片的校验
                if (result) {
                    if (img.length > 0) {
                        var add_img = [];
                        img.each(function (i) {
                            var list = new Object();
                            list.id = $(this).attr("data-id");
                            list.url = $(this).find("img").attr("src");
                            list.size = $(this).find("img").attr("data-size");
                            add_img[i] = list;
                        });
                    }
                }

                if (result) {
                    that.err.empty();

                    var data_list = new Object();
                    data_list.title = title;
                    data_list.content = content;
                    data_list.img = JSON.stringify(add_img);
                    data_list._xsrf = $('input[name="_xsrf"]').val();
                    data_list.clicked = true;

                    jQuery.ajax({
                        type: "POST",
                        url: "/topic/create/" + topic,
                        data: data_list,
                        dataType: "JSON",
                        success: function (data) {
                            var stat = data.stat;

                            if (stat == "ok") {
                                window.location.href = "/topic/detail/" + data.topic_id + "/" + data.topic_user_id;
                            } else {
                                alert(data.msg);
                            }
                            _self.attr("disabled", false);
                        },
                        error: function () {
                            _self.attr("disabled", false);
                        }
                    });
                } else {
                    _self.attr("disabled", false);
                }
            }
        });

        //分类切换
        $('.condition').click(function(){
            var _self = $(this);
            if(!_self.hasClass("condition-active")){
                $('.condition').removeClass("condition-active");
                _self.addClass("condition-active");

                var tab = $('.tab-active').data("id"),
                    condition = _self.data("id"),
                    order = $('.order-active').data("id"),
                    page = 1;
                $('input[name="page"]').attr("value", 1);
                that.loadTopic(page, tab, condition, order);
            }
        });

        //排序切换数据
        $('.order').mouseover(function(e){
            e.stopPropagation();
            $(this).css("background-position", "40px -113px");
            $('.order-list').slideDown();
        });

        $('body').click(function(){
            $('.order').css("background-position", "40px -84px");
            $('.order-list').slideUp();
        });

        $('.order-type').click(function(e){
            e.stopPropagation();
            var _self = $(this);
            if(!_self.hasClass("order-active")){
                $('.order-type').removeClass("order-active");
                _self.addClass("order-active");

                var tab = $('.tab-active').data("id"),
                    condition = $('.condition-active').data("id"),
                    order = _self.data("id"),
                    page = 1;
                $('input[name="page"]').attr("value", 1);

                $('.order').css("background-position", "40px -84px");
                $('.order-list').slideUp();

                that.loadTopic(page, tab, condition, order);
            }
        });

        //话题详情页回复操作
        $('.topic_detail').on('click', '.reply', function(){
            if (!getCookie()){
                $('#J-login').click();
            } else {
                var id = $(this).closest(".topic-list").data("id"),
                    name = $(this).closest(".topic-list").data("name");
                $('input[name="commentedObject"]').attr("value", id);
                $('.topic-desc-content').attr("placeholder", "回复: " + name);
            }
        });

        //list页 按钮操作
        $('#topic').on('mouseover', '.topic-list', function(){
            $(this).find('.manageOperatingBtn').show();
        }).on('mouseout', '.topic-list', function(){
            $(this).find('.manageOperatingBtn').hide();
        });

        $('.commentBtn').click(function(){
            if (!getCookie()){
                $('#J-login').click();
            } else {
                var _self = $(this);
                _self.attr("disabled", true);

                var topic_id = $('input[name="topic_id"]').val(),
                    parent_id = $('input[name="commentedObject"]').val(),
                    content = that.content.val().replace(/\s+/g,""),
                    content = that.replace_em(content),
                    img = $('.upload-descImg-list li'),
                    result = true;

                //跟帖内容校验
                if (content.length < 5) {
                    that.content.focus();
                    that.err.text("请输入话题内容, 最少5个字！");
                    result = false;
                }

                //描述图片的校验
                if (result) {
                    if (img.length > 0) {
                        var add_img = [];
                        img.each(function (i) {
                            var list = new Object();
                            list.id = $(this).attr("data-id");
                            list.url = $(this).find("img").attr("src");
                            list.size = $(this).find("img").attr("data-size");
                            add_img[i] = list;
                        });
                    }
                }

                if (result) {
                    that.err.empty();

                    var data_list = new Object();
                    data_list.content = content;
                    data_list.img = JSON.stringify(add_img);
                    data_list._xsrf = $('input[name="_xsrf"]').val();

                    jQuery.ajax({
                        type: "POST",
                        url: "/topic/reply/create/" + topic_id + "/" + parent_id,
                        data: data_list,
                        dataType: "JSON",
                        success: function (data) {
                            var stat = data.stat;

                            if (stat == "ok") {
                                var list = data.reply_list[0];

                                if (list.parent == "") {
                                    var parent = "";
                                } else {
                                    var html_2 = $('#J-model-topic-comment2').html();
                                    var parent = that.toReplaceParentCommentModel(html_2, list.parent);
                                }

                                var html = $('#J-model-topic-comment').html();
                                list.vote_judge = 1;
                                var templates = that.toReplaceModel_comment(html, list, parent);
                                $('#detail_topic_comment').append(templates);
                                $('input[name="commentedObject"]').val("0");
                                $('.topic-desc-content').val("").attr("placeholder", "请输入跟帖内容，至少5个字");
                                $('.upload-descImg-list').empty();
                            } else {
                                alert(data.msg);
                            }
                            _self.attr("disabled", false);
                        },
                        error: function () {
                            _self.attr("disabled", false);
                        }
                    });
                } else {
                    _self.attr("disabled", false);
                }
            }
        });

        //话题详情页回复操作--点赞
        $('.topic_detail').on('click', '.vote', function(){
            if (!getCookie()){
                $('#J-login').click();
            } else {
                var _self = $(this);
                var comment_id = $(this).closest(".topic-list").data("id");
                var topic_id = (comment_id == "0") ? $('input[name="topic_id"]').val() : comment_id,
                    topic_type = (comment_id == "0") ? 1 : 2,
                    sns_type = 1,
                    opration = $(this).attr("data-vote");

                jQuery.ajax({
                    type: "GET",
                    url: '/topic/sns/' + topic_id + '/' + sns_type + '/' + topic_type + '/' + opration,
                    data: {},
                    dataType: "JSON",
                    success: function (data) {
                        var stat = data.stat;

                        if (stat == "ok") {
                            if (opration == 1) {
                                _self.attr("data-vote", 0);
                                _self.find(".approval").text(parseInt(_self.find(".approval").text()) + 1);
                                _self.removeClass("voteNO").addClass("voteYES");
                            } else {
                                _self.attr("data-vote", 1);
                                _self.removeClass("voteYES").addClass("voteNO");
                                _self.find(".approval").text(parseInt(_self.find(".approval").text()) - 1);
                            }
                        } else {
                            alert(data.msg);
                        }
                    },
                    error: function () {
                    }
                });
            }
        });

        //话题list页，置顶，精华，删除的操作
        $('#topic').on('click', '.manageOperatingBtn', function(){
            var _self = $(this);
            _self.attr("disabled", true);
            var f = confirm("确认要"+_self.val()+"吗？");

            if(f){
                var topic_id, opration, type;

                topic_id = _self.closest('li').attr("data-id");
                if(_self.hasClass("toDelete")){
                    opration = "delete";
                }else if(_self.hasClass("toEssence")){
                    opration = "essence";
                }else if(_self.hasClass("toTop")){
                    opration = "top";
                }
                type = _self.attr("data-stat");

                jQuery.ajax({
                    type: "GET",
                    url: '/admin/topic/operation/' + topic_id + '/' + opration + '/' + type,
                    data: {},
                    dataType: "JSON",
                    success: function (data) {
                        _self.attr("disabled", false);
                        var stat = data.stat;

                        if (stat == "ok"){
                            if(_self.hasClass("toDelete")){
                                _self.closest('li').remove();
                            }else if(_self.hasClass("toEssence")){
                                if(type==1) {
                                    _self.closest('li').find('.topic-list-title').prepend('<p class="essence">精</p>');
                                    _self.attr("data-stat", "0").val("取消精华");
                                }else{
                                    _self.closest('li').find('.essence').remove();
                                    _self.attr("data-stat", "1").val("精华");
                                }
                            }else if(_self.hasClass("toTop")) {
                                if (type == 1) {
                                    _self.closest('li').find('.topic-list-title').prepend('<p class="top">顶</p>');
                                    _self.attr("data-stat", "0").val("取消置顶");
                                } else {
                                    _self.closest('li').find('.top').remove();
                                    _self.attr("data-stat", "1").val("置顶");
                                }
                            }
                        } else {
                            alert(data.msg);
                        }
                    },
                    error: function (){
                        _self.attr("disabled", false);
                    }
                });
            }else{
                _self.attr("disabled", false);
            }
        });

        //活跃榜维度切换
        $('.this-week').click(function(){
            if(!$(this).hasClass("hy-tab-active")){
                $('.this-month').removeClass("hy-tab-active");
                $(this).addClass("hy-tab-active");

                $('#week-list-part').removeClass("hide");
                $('#month-list-part').addClass("hide");
            }
        });
        $('.this-month').click(function(){
            if(!$(this).hasClass("hy-tab-active")){
                $('.this-week').removeClass("hy-tab-active");
                $(this).addClass("hy-tab-active");

                $('#month-list-part').removeClass("hide");
                $('#week-list-part').addClass("hide");
            }
        });

        //翻页方法在此
        $('#J-manage-page').on("click", ".pageNum", function(){
            var page = $(this).text();
            $('input[name="page"]').attr("value", page);
            that.pageChangeData(page);
        });
        $('#J-manage-page').on("click", ".page-prev", function(){
            var page = parseInt($('input[name="page"]').val())-1;
            $('input[name="page"]').attr("value", page);
            that.pageChangeData(page);
        });
        $('#J-manage-page').on("click", ".page-next", function(){
            var page = parseInt($('input[name="page"]').val())+1;
            $('input[name="page"]').attr("value", page);
            that.pageChangeData(page);
        });
        $('#J-manage-page').on("click", ".toJump", function(){
            var page = parseInt($('input[name="toPage"]').val());
            var total_page = parseInt($('input[name="total_page"]').val());
            if(page<=total_page){
                $('input[name="page"]').attr("value", page);
                that.pageChangeData(page);
            }else{
                alert("请输入正确页数！");
                $('input[name="toPage"]').attr("value", "");
            }
        });
    },

    //加载话题数据
    loadTopic: function(page, tab, condition, order){
        var that = this;

        jQuery.ajax({
            type: "GET",
            url: '/topic/category/' + tab + '/' + order,
            data: {
                page: page,
                is_essence: condition
            },
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok"){
                    $('#topic').empty();
                    var list = data.list;
                    $.each(list, function(i){
                        var html = $('#J-model-topic-list').html();
                        var templates = that.toReplaceModel(html, list[i]);
                        $('#topic').append(templates);
                    });
                    parseInt(data.total_page) > 1 ? that.loadPage(data.cur_page, data.total_page) : $('#J-manage-page').empty();
                } else {
                    alert(data.msg);
                }
            },
            error: function (){
            }
        });
    },

    //加载话题评论
    loadTopicComment: function(page){
        var that = this;
        var topic_id = $('input[name="topic_id"]').val();

        jQuery.ajax({
            type: "GET",
            url: '/topic/reply/' + topic_id + '/',
            data: {
                page: page
            },
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok"){
                    $('.topic_detail').empty();
                    var list = data.reply_list;

                    $.each(list, function(i) {
                        if (list[i].parent == "") {
                            var parent = "";
                        } else {
                            var html_2 = $('#J-model-topic-comment2').html();
                            var parent = that.toReplaceParentCommentModel(html_2, list[i].parent);
                        }

                        var html = $('#J-model-topic-comment').html();
                        var templates = that.toReplaceModel_comment(html, list[i], parent);
                        $('#detail_topic_comment').append(templates);
                    });
                    parseInt(data.total_page) > 1 ? that.loadPage(data.cur_page, data.total_page) : $('#J-manage-page').empty();
                } else {
                    alert(data.msg);
                }
            },
            error: function (){
            }
        });
    },

    //上传图片
    addPhotos: function(uploader, i){
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            //maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('.upload-descImg-list li:eq(' + i + ')').attr("data-id", file.id);
                    $('.upload-descImg-list li:eq(' + i + ')').find("img").attr({"src": file.url, "data-size": file.size});
                    i++;
                });
            },
            send: function (e, data) {
                var close = '<a href="javascript:;" onclick="$(this).closest(\'li\').remove()" class="upload-descImg-close"></a>',
                    img = '<img src="/static/skin/images/user-loading.gif" data-size="" alt="">';
                var li = '<li data-id="">'+ close + img +'</li>';
                $('.upload-descImg-list').append(li);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    },

    //加载页数
    loadPage: function(page, total_page){
        $('input[name="total_page"]').attr("value", total_page);
        var i, pageList="", allPageList="";
        var pageHtml = {
            total: '<p class="total-page">共' + total_page + '页</p>',
            prev: '<a href="#" class="icon page-prev"></a>',
            next: '<a href="#" class="icon page-next"></a>',
            point: '<p>...</p>',
            toPage: '<p class="goPage clearfix"><ins>去第</ins><input type="text" name="toPage" value=""><ins>页</ins></p>',
            btn: '<a href="#" class="toJump">跳转</a>',
            activePage: '<p class="page-active">' + page + '</p>',
            page: '<a href="#" class="pageNum">{{number}}</a>',
            firstPage: '<a href="#" class="pageNum">1</a>',
            lastPage: '<a href="#" class="pageNum">' + total_page + '</a>'
        }

        if(total_page<=5){
            for(i=1; i<=total_page; i++){
                pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
            }
        }else{
            if(page<4){
                for(i=1; i<=4; i++){
                    pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
                }
                pageList+= pageHtml.point + pageHtml.lastPage;
            }else if(page>(total_page-4)){
                for(i=(total_page-4); i<=total_page; i++){
                    pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
                }
                pageList = pageHtml.firstPage + pageHtml.point + pageList;
            }else{
                for(i=(page-1); i<=(page+1); i++){
                    pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
                }
                pageList = pageHtml.firstPage + pageHtml.point + pageList + pageHtml.point + pageHtml.lastPage;
            }
        }

        if(page==1){
            allPageList = pageList + pageHtml.next;
        }else if(page==total_page){
            allPageList = pageHtml.prev + pageList;
        }else{
            allPageList = pageHtml.prev + pageList + pageHtml.next;
        }
        allPageList+=  pageHtml.toPage + pageHtml.btn;
        $('#J-manage-page').html(allPageList);
    },
    pageChangeData: function(page){
        var tab = $('.tab-active').data("id"),
            condition = $('.condition-active').data("id"),
            order = $('.order-active').data("id"),
            pageType = $('input[name="pageType"]').val();

        if(pageType=="LIST") {
            this.loadTopic(page, tab, condition, order);
        }else if(pageType=="DETAIL"){
            this.loadTopicComment(page);
        }
    },

    //模板页面，数据替换在此
    toReplaceModel: function(html, list){
        html = html.replace("{{topic_id}}", list.Fid);
        html = html.replace("{{Fis_top}}", list.Fis_top ? '<p class="top">顶</p>' : "");
        html = html.replace("{{Fis_essence}}", list.Fis_essence ? '<p class="essence">精</p>' : "");
        html = html.replace("{{topic_id}}", list.Fid);
        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{title}}", list.Ftitle);
        html = html.replace("{{hasImg}}", list.photo==1 ? '<p class="topic-icon hasImg"></p>' : "");
        html = html.replace("{{content}}", list.Fcontent);

        if(list.photo==1) {
            var imgs = list.imgs, imgsHtml = "", images_link = "";
            $.each(imgs, function (k) {
                imgsHtml = '<img src="' + imgs[k][1] + '" data-id="' + imgs[k][0] + '" alt="">';
                images_link = images_link + '<a href="/topic/detail/' + list.Fid + '/' + list.Fuser_id + '" class="topic-desc-link" target="_blank">' + imgsHtml + '</a>';
            });
            html = html.replace("{{descImg}}", '<div class="topic-desc-img clearfix">' + images_link + '</div>');
        }else{
            html = html.replace("{{descImg}}", '');
        }

        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{url}}", list.head_url);
        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{name}}", list.nick_name);
        html = html.replace("{{time}}", list.time);
        html = html.replace("{{topic_id}}", list.Fid);
        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{comment}}", list.Ftotal_assess);
        html = html.replace("{{view}}", list.Fpage_view);

        var toTop = '', toEssence = '', toDelete = '<input type="button" class="manageOperatingBtn toDelete" data-stat="1" value="删除">';
        if(list.is_admin){
            if(list.Fis_top){
                toTop = '<input type="button" class="manageOperatingBtn toTop" data-stat="0" value="取消置顶">';
            }else{
                toTop = '<input type="button" class="manageOperatingBtn toTop" data-stat="1" value="置顶">';
            }
            if(list.Fis_top){
                toEssence = '<input type="button" class="manageOperatingBtn toEssence" data-stat="0" value="取消精华">';
            }else{
                toEssence = '<input type="button" class="manageOperatingBtn toEssence" data-stat="1" value="精华">';
            }
            html = html.replace("{{operating}}", toDelete + toEssence + toTop);5
        }else{
            html = html.replace("{{operating}}", "");
        }

        return html;
    },
    toReplaceParentCommentModel: function(html, list){
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{name}}", list.nick_name);
        html = html.replace("{{time}}", list.time);
        html = html.replace("{{floor}}", list.parent_index);
        html = html.replace("{{content}}", list.parent_content);

        if(list.images.length>0) {
            var imgs = list.images, imgsHtml = "";
            $.each(imgs, function (k) {
                imgsHtml = imgsHtml + '<img src="' + imgs[k].img + '" alt="">';
            });
            html = html.replace("{{descImg}}", '<div class="top-detail-descImg clearfix">' + imgsHtml + '</div>');
        }else{
            html = html.replace("{{descImg}}", '');
        }

        return html;
    },
    toReplaceModel_comment: function(html, list, parent){
        html = html.replace("{{id}}", list.Fid);
        html = html.replace("{{name}}", list.nick_name);
        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{head_url}}", list.head_url);
        html = html.replace("{{user_id}}", list.Fuser_id);
        html = html.replace("{{name}}", list.nick_name);
        html = html.replace("{{time}}", list.time);
        html = html.replace("{{floor}}", list.index);
        html = html.replace("{{commented_object}}", parent);
        html = html.replace("{{content}}", list.content);

        if(list.images.length>0) {
            var imgs = list.images, imgsHtml = "";
            $.each(imgs, function (k) {
                imgsHtml = imgsHtml + '<img src="' + imgs[k].img + '" alt="">';
            });
            html = html.replace("{{descImg}}", '<div class="top-detail-descImg clearfix">' + imgsHtml + '</div>');
        }else{
            html = html.replace("{{descImg}}", '');
        }

        html = html.replace("{{vote}}", list.vote_judge==1 ? "voteNO" : "voteYES");
        html = html.replace("{{vote_judge}}", list.vote_judge);
        html = html.replace("{{assist}}", list.Fpraise);

        return html;
    },
    replace_em: function(content){
        content = content.replace(/</g, '&lt;');
        content = content.replace(/>/g, '&gt;');
        content = content.replace(/\s+/g, '<br/>');
        content = content.replace(/\[em_([0-9]*)\]/g, '<img src="/static/skin/js/plug/face/$1.gif" border="0">');
        return content;
    },
    replace_em_init: function(content){
        content = content.replace(/&lt;/g, '<');
        content = content.replace(/&gt;/g, '>');
        return content;
    }
}

//登录校验
function getCookie() {
    function escape(s) {
        return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
    }
    var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape('loginuser') + '=([^;]*)'));
    return match ? match[1] : null;
}