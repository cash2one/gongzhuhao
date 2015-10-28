/**
 * Created by hujunhao on 15/1/12.
 */

var init = {
    loadQaList: function(type, order, page){
        $('.comments-list').html('<img src="/static/skin/images/public/loading-zenmez.gif" style="width: 120px; height: 120px; margin: 50px auto; display: block;" alt="">');
        $('#J-manage-page').empty();

        var data_list = new Object();

        data_list.type = type;
        data_list.order = order;
        data_list.page = page;
        data_list._xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/qa/question/list",
            data: data_list,
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(stat=="ok") {
                    $('.comments-list').empty();
                    var list = data.list,
                        page = data.cur_page,
                        total_page = data.total_page;

                    $.each(list, function(i){
                        var html = $('#J-model-qa').html();
                        var templates = toReplaceModel(html, list[i]);

                        $('.comments-list').append(templates);
                    });
                    parseInt(total_page) > 1 ? init.loadPage(page, total_page) : $('#J-manage-page').empty();

                }else{
                    alert(data.msg);
                }
            },
            error: function () {
            }
        });
    },
    loadPage: function(page, total_page){
        $('input[name="total_page"]').attr("value", total_page);
        var i, pageList="", allPageList="";
        var pageHtml = {
            total: '<p class="total-page">共' + total_page + '页</p>',
            prev: '<a href="javascript:void(0)" class="icon page-prev"></a>',
            next: '<a href="javascript:void(0)" class="icon page-next"></a>',
            point: '<p>...</p>',
            toPage: '<p class="goPage clearfix"><ins>去第</ins><input type="text" name="toPage" value=""><ins>页</ins></p>',
            btn: '<a href="javascript:void(0)" class="toJump">跳转</a>',
            activePage: '<p class="page-active">' + page + '</p>',
            page: '<a href="javascript:void(0)" class="pageNum">{{number}}</a>',
            firstPage: '<a href="javascript:void(0)" class="pageNum">1</a>',
            lastPage: '<a href="javascript:void(0)" class="pageNum">' + total_page + '</a>'
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
    }
}

/* 模板加载需先加载空模板 */
function toReplaceModel(html, list){
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{head}}", list.user_photo);
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{title}}", list.title);
    html = html.replace("{{user_id}}", list.user_id);
    html = html.replace("{{nick}}", list.nick);
    html = html.replace("{{gmt_created}}", list.gmt_created);
    html = html.replace("{{cate}}", list.cate);
    html = html.replace("{{id}}", list.id);
    html = html.replace("{{comments_count}}", list.comments_count);
    html = html.replace("{{view_times}}", list.view_times);
    html = html.replace("{{question_desc}}", list.question_desc);

    var more = '<a href="/qa/detail/'+list.id+'/" class="qa-desc-more" style="margin-left: 20px;">更多>></a>';
    var desc = list.question_desc.length > 130 ? list.question_desc.substring(0, 110)+ "..." + more : list.question_desc;
    html = html.replace("{{question_desc}}", desc);

    return html;
}

$(document).ready(function(){

    //活跃榜维度切换
    $('.this-week').click(function(){
        if(!$(this).hasClass("tab-active")){
            $('.this-month').removeClass("tab-active");
            $(this).addClass("tab-active");

            $('#week-list-part').removeClass("hide");
            $('#month-list-part').addClass("hide");
        }
    });
    $('.this-month').click(function(){
        if(!$(this).hasClass("tab-active")){
            $('.this-week').removeClass("tab-active");
            $(this).addClass("tab-active");

            $('#month-list-part').removeClass("hide");
            $('#week-list-part').addClass("hide");
        }
    });

    //问答--upload上传图片
    $('#fileupload-qa').click(function(){
        var uploader = $("#J-qa-formFile");
        var i = $('.qa-img-list li').length;
        addPhoto(uploader, i);
    });

    //问答上传毕业照
    function addPhoto(uploader, i) {
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            //maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('.qa-img-list li:eq(' + i + ')').attr("data-id", file.id);
                    $('.qa-img-list li:eq(' + i + ')').find("img").attr("src", file.url);
                    i++;
                });
            },
            send: function (e, data) {
                var img = '<img src="/static/skin/images/user-loading.gif" alt="">';
                var li = '<li data-id="">'+ img +'</li>';
                $('.qa-img-list').append(li);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    }

    //问答详情页回答图片上传
    $('#fileupload-qa-detail').click(function () {
        var uploader = $("#J-qa-detail-formFile");
        var i = $('.detail-comments-img-list li').length;
        addCommentsPhoto(uploader, i);
    });

    //问答上传毕业照
    function addCommentsPhoto(uploader, i) {
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            //maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('.detail-comments-img-list li:eq(' + i + ')').attr("data-id", file.id);
                    $('.detail-comments-img-list li:eq(' + i + ')').find("img").attr("src", file.url);
                    i++;
                });
            },
            send: function (e, data) {
                var img = '<img src="/static/skin/images/user-loading.gif" alt="">';
                var li = '<li data-id="">'+ img +'</li>';
                $('.detail-comments-img-list').append(li);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    }

    //问答类型切换
    $('.qa-type').click(function(){
        var _self = $(this);
        var type = "", order = "", page = "";

        type = _self.attr("data-type");

        $('.qa-type').each(function(){
            $(this).removeClass("qa-type-active");
        });
        _self.addClass("qa-type-active");

        //问答排序类型
        $('.comment-tab').each(function(k){
            $(this).hasClass("comment-tab-active") ? order = $(this).attr("data-order") : "";
        });

        //页数
        page = $('input[name="page"]').val();

        //初始化加载问答数据
        init.loadQaList(type, order, page);
    });

    //问答排序切换
    $('.comment-tab').click(function(){
        var _self = $(this);
        var type = "", order = "", page = "";

        order = _self.attr("data-order");

        $('.comment-tab').each(function(){
            $(this).removeClass("comment-tab-active");
        });
        _self.addClass("comment-tab-active");

        //问答类型
        $('.qa-type').each(function(){
            $(this).hasClass("qa-type-active") ? type = $(this).attr("data-type") : "";
        });

        //页数
        page = $('input[name="page"]').val();

        //初始化加载问答数据
        init.loadQaList(type, order, page);
    });

    //提交问题
    $('.comments').click(function(){
        var _self = $(this);
        _self.attr("disabled", true);
        var question_type_id, title, question_desc;
        var result = true;

        //问题分类选择
        question_type_id = $('.qa-type-select').val();
        if (question_type_id == "-1") {
            result = false;
            alert("请选择问题分类！");
        }

        if (result) {
            //问题标题
            title = $('input[name="general"]').val();
            if (title == "") {
                result = false;
                alert("请添加问题标题！");
            }
        }

        if (result) {
            //问题描述
            question_desc = $('#qa_desc').val();
            if (question_desc == "") {
                result = false;
                alert("请添加问题描述！");
            }
        }

        if (result) {
            var qa_img = $('.qa-img-list li');
            if (qa_img.length != 0) {
                var add_img = [];
                qa_img.each(function (i) {
                    var list = new Object();
                    list.id = $(this).attr("data-id");
                    list.src = $(this).find("img").attr("src");

                    add_img[i] = list;
                });
            }
        }

        if (result) {
            var data_list = new Object();

            data_list.question_type_id = question_type_id;
            data_list.title = title;
            data_list.question_desc = question_desc;
            data_list.add_img = JSON.stringify(add_img);
            data_list._xsrf = $('input[name="_xsrf"]').val();

            jQuery.ajax({
                type: "POST",
                url: "/qa/question/create",
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        window.location.href = "/qa/detail/" + data.id + "/";
                    } else {
                        alert(data.msg);
                    }
                    _self.attr("disabled", false);
                },
                error: function (){
                }
            });
        } else {
            _self.attr("disabled", false);
        }
    });

    //问答详情页 评论内容提交
    $('.upload-comments-btn').click(function(){
        $(this).attr("disabled", true);
        var target_user_id = "0";   //被评论用户的id
        var parent_id = "0";    //一级回复的id
        var question_id = $('input[name="question_id"]').val();   //问题的id
        var content = $('#answer').val();     //评论的内容
        var _xsrf = $('input[name="_xsrf"]').val();
        var type = "first-comment";

        var comment_img = $('.detail-comments-img-list li');
        if (comment_img.length != 0) {
            var add_img = [];
            comment_img.each(function (i) {
                var list = new Object();
                list.id = $(this).attr("data-id");
                list.src = $(this).find("img").attr("src");

                add_img[i] = list;
            });
        }

        if(content!=""){
            var data_list = new Object();

            data_list.target_user_id = target_user_id;
            data_list.parent_id = parent_id;
            data_list.question_id = question_id;
            data_list.content = content;
            data_list.add_img = JSON.stringify(add_img);
            data_list._xsrf = _xsrf;

            comments(data_list, type);
        }else{
            alert("评论内容不能为空");
        }
        $(this).attr("disabled", false);
    });

    //二级评论提交
    $('.reply-btn').click(function(e){
        e.stopPropagation();
        var _self = $(this);

        var target_user_id = _self.closest('.reply-input-part').find('input[name="target_user_id"]').val();   //被评论用户的id
        var parent_id = _self.closest(".dfc-li").attr("data-id");    //一级回复的id
        var question_id = $('input[name="question_id"]').val();   //问题的id
        var content = _self.closest('.reply-input-part').find('.reply-content').val();     //评论的内容
        var _xsrf = $('input[name="_xsrf"]').val();
        var type = "second-comment";
        var node = _self.closest(".second-comments-part").find(".detail-second-comments");

        if(content!=""){
            var data_list = new Object();

            data_list.target_user_id = target_user_id;
            data_list.parent_id = parent_id;
            data_list.question_id = question_id;
            data_list.content = content;
            data_list._xsrf = _xsrf;

            comments(data_list, type, node);
            _self.closest('.reply-input-part').find('.reply-content').val("");
        }else{
            alert("评论内容不能为空");
        }
    });

    //一、二级评论提交
    function comments(data_list, type, node){
        jQuery.ajax({
            type: "POST",
            url: "/qa/answer/create",
            data: data_list,
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if(stat=="ok"){
                    var list = data.list;
                    if(type=="first-comment"){
                        firstComments(list, node);
                    }else if(type=="second-comment"){
                        var html = $('#J-model-second-comment').html();
                        var templates = toReplaceModel_sc(html, list);

                        node.append(templates);
                    }
                }else {
                    alert(data.msg);
                }

            },
            error: function () {
            }
        });
    }

    //加载一级评论模板
    function firstComments(list, node){
        var html = $('#J-model-first-comment').html();
        var templates = toReplaceModel_fc(html, list);

        $('.detail-first-comments').append(templates);
        $('#commentCount').text(parseInt($('#commentCount').text())+1);
        $('#answer').val("");
        $('.detail-comments-img-list').empty();
    }

    /* 模板加载需先加载空模板--一级评论 */
    function toReplaceModel_fc(html, list){
        html = html.replace("{{id}}", list.id);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{photo}}", list.photo);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{nick}}", list.nick);
        html = html.replace("{{answer}}", list.answer);

        var imgs = list.imgs, answer_img = "";
        $.each(imgs, function(i){
            var li = '<li>' +
                '<img src="' + imgs[i].show_url + '" alt="">' +
                '</li>';
            answer_img+=li;
        });

        html = html.replace("{{imgs}}", answer_img);
        html = html.replace("{{gmt_created}}", list.gmt_created);

        return html;
    }

    /* 模板加载需先加载空模板--2级评论 */
    function toReplaceModel_sc(html, list){
        html = html.replace("{{id}}", list.id);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{photo}}", list.photo);
        html = html.replace("{{user_id}}", list.user_id);
        html = html.replace("{{nick}}", list.nick);
        html = html.replace("{{answer}}", list.answer);
        html = html.replace("{{gmt_created}}", list.gmt_created);

        return html;
    }

    //一级评论的回复展现和隐藏
    $('.detail-first-comments').on('click', '.first-reply', function(){
        var _self = $(this);
        var s = _self.closest(".first-comments-info").find(".second-comments-part"),
            r = _self.closest(".first-comments-info").find(".reply-input-part"),
            target_user_id = _self.closest(".dfc-li").attr("data-userid"),
            u = _self.closest(".first-comments-info").find("input[name='target_user_id']");

        if(s.hasClass("hide")){
            r.show().removeClass("hide");
            s.slideToggle().removeClass("hide");
            u.attr("value", target_user_id);
        }else{
            if(r.hasClass("hide")){
                r.show().removeClass("hide");
                u.attr("value", target_user_id);
            }else{
                s.slideToggle().addClass("hide");
                r.hide().addClass("hide");
            }
        }
    });

    //2级评论的回复展现和隐藏
    $('.detail-first-comments').on('click', '.second-reply', function(){
        var _self = $(this);
        var r = _self.closest(".second-comments-part").find(".reply-input-part"),
            target_user_id = _self.closest(".dsc-li").attr("data-userid"),
            name = _self.closest(".dsc-li").find(".first-user-name").text(),
            u = _self.closest(".second-comments-part").find("input[name='target_user_id']"),
            t = _self.closest(".second-comments-part").find(".reply-content");

        r.slideDown();
        u.attr("value", target_user_id);
        t.attr("placeholder", "回复 "+name);
    });

    $('.qa-type-select').change(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.qa-general').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.qa-desc').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.comment-content').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });
    $('.reply-content').focus(function(){
        if (!getCookie()){
            $('#J-login').click();
        }
    });

    //qa-list-more
    /*
    $('.comments-list').on('click', '.qa-desc-more', function(){
        var desc = $(this).closest(".question_desc").attr("data-content");
        $(this).closest(".question_desc").text(desc);
    });
    */

    //登录校验
    function getCookie() {
        function escape(s) {
            return s.replace(/([.*+?\^${}()|\[\]\/\\])/g, '\\$1');
        }
        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape('check_loginuser') + '=([^;]*)'));
        return match ? match[1] : null;
    }

    //翻页方法在此
    $('#J-manage-page').on("click", ".pageNum", function(){
        var page = $(this).text();
        $('input[name="page"]').attr("value", page);
        pageChangeData(page);
    });
    $('#J-manage-page').on("click", ".page-prev", function(){
        var page = parseInt($('input[name="page"]').val())-1;
        $('input[name="page"]').attr("value", page);
        pageChangeData(page);
    });
    $('#J-manage-page').on("click", ".page-next", function(){
        var page = parseInt($('input[name="page"]').val())+1;
        $('input[name="page"]').attr("value", page);
        pageChangeData(page);
    });
    $('#J-manage-page').on("click", ".toJump", function(){
        var page = parseInt($('input[name="toPage"]').val());
        var total_page = parseInt($('input[name="total_page"]').val());
        if(page<=total_page){
            $('input[name="page"]').attr("value", page);
            pageChangeData(page);
        }else{
            alert("请输入正确页数！");
            $('input[name="toPage"]').attr("value", "");
        }
    });

    function pageChangeData(page){
        var type = "", order = "";

        //问答类型
        $('.qa-type').each(function(){
            $(this).hasClass("qa-type-active") ? type = $(this).attr("data-type") : "";
        });

        //问答排序类型
        $('.comment-tab').each(function(){
            $(this).hasClass("comment-tab-active") ? order = $(this).attr("data-order") : "";
        });

        init.loadQaList(type, order, page);
    }

    //问答详情页大图展示
    $('.showBigImg').click(function(){
        var imgSrc = $(this).attr("data-src");
        $('.bigImgShow img').attr("src", imgSrc);

        var width = $(window).width(),  //浏览器当前窗口可视区域宽度
            v_height = $(window).height(),  //浏览器当前窗口可视区域高度
            d_height = $(document).height();  //浏览器当前窗口文档的高度

        //黑色半透明遮罩层显示
        $('body').append('<div class="cover"></div>');
        $('.cover').css({"width": width, "height":d_height}).show();

        var img_heigth = 610;
        var img_width = 990;
        if(parseInt(img_heigth)>=parseInt(v_height)){
            var top = 0;
        }else{
            var top = (parseInt(v_height)-parseInt(img_heigth))/2;
        }
        var left = (parseInt(width)-parseInt(img_width))/2;
        $('.bigImgShow').css({"left":left, "max-height":v_height, "top":top}).slideDown();
    });

    $('body').on('click', '.cover', function(){
        $('.bigImgShow img').attr("src", "");
        $('.bigImgShow').hide();
        $(this).remove();
    });
    $('.bigImgShow').click(function(){
        $('.bigImgShow img').attr("src", "");
        $(this).hide();
        $('.cover').remove();
    });
});