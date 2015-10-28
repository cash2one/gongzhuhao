/*
* hujunhao
* 2015.1.19
*/

var init = {
    diaryLoad: function(share_type, house_style, design_style, area, order, page){
        var _xsrf = $('input[name="_xsrf"]').val();
        var loadPart;

        if(share_type=="1"){
            var url = "/share";
            loadPart = $('.diary-list-part');
        }else if(share_type=="2"){
            var url = "/share/album";
            loadPart = $('.list-wrap');
        }
        loadPart.html('<img src="/static/skin/images/public/loading-zenmez.gif" style="width: 120px; height: 120px; margin: 50px auto; display: block;" alt="">');
        $('#J-manage-page').empty();

        jQuery.ajax({
            type: "POST",
            url: url,
            data: {house_style:house_style, design_style:design_style, area:area, order:order, page:page, _xsrf:_xsrf},
            dataType: "JSON",
            success: function(data){
                var page = data.page,
                    total_page = data.total_page;

                loadPart.empty();

                if(share_type=="1"){
                    var articles = data.articles;
                    $.each(articles, function(i){
                        var html = $('#J-model-share-diary').html();
                        var templates = toReplaceModel_diary(html, articles[i]);

                        $('.diary-list-part').append(templates);
                    });
                }else if(share_type=="2"){
                    var byzs = data.byzs;
                    $.each(byzs, function(i){
                        var html = $('#J-model-share-photo').html();
                        var templates = toReplaceModel_photo(html, byzs[i]);

                        $('.list-wrap').append(templates);
                    });
                }
                parseInt(total_page) > 1 ? init.loadPage(page, total_page) : $('#J-manage-page').empty();
            },
            error: function(){

            }
        });
    },
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
    }
}

/* 模板加载需先加载空模板(分享日记) */
function toReplaceModel_diary(html, articles){
    html = html.replace("{{user_id}}", articles.user_id);
    html = html.replace("{{user_photo}}", articles.user_photo);
    html = html.replace("{{user_name}}", articles.user_name);
    html = html.replace("{{user_name}}", articles.user_name);
    html = html.replace("{{user_id}}", articles.user_id);
    html = html.replace("{{title}}", articles.title);
    html = html.replace("{{article_count}}", articles.article_count);
    html = html.replace("{{view_times}}", articles.view_times);
    html = html.replace("{{assist_count}}", articles.assist_count);
    html = html.replace("{{comments_count}}", articles.comments_count);
    html = html.replace("{{total_price}}", articles.total_price);
    html = html.replace("{{byz_count}}", articles.byz_count);
    html = html.replace("{{community_name}}", articles.community_name);
    html = html.replace("{{house_type_name}}", articles.house_type_name);
    html = html.replace("{{m2}}", articles.m2);
    html = html.replace("{{stage_name}}", articles.stage_name);
    html = html.replace("{{content}}", articles.content);

    var more = '<a href="javascript:void(0)" class="qa-desc-more" style="margin-left: 20px;">更多>></a>';
    var content = articles.content.length > 180 ? articles.content.substring(0, 170)+"..."+ more : articles.content;
    html = html.replace("{{content}}", content);

    var img_list = "";
    $.each(articles.stage_images, function(i){
        var li = '<li class="diary-img">' +
            '<a href="/member/decorate_article/edit/' + articles.user_id + '" target="_blank">' +  '<img src="'+ articles.stage_images[i] +'" alt="">' + '</a>'
        '</li>';
        img_list+=li;
    });
    html = html.replace("{{img_list}}", img_list);
    html = html.replace("{{gmt_modified}}", articles.gmt_modified);

    return html;
}

/* 模板加载需先加载空模板(分享毕业照) */
function toReplaceModel_photo(html, byzs){
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{show_img}}", byzs.show_img);
    //html = html.replace("{{assist_count}}", byzs.assist_count);
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{user_photo}}", byzs.user_photo);
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{title}}", byzs.title);
    html = html.replace("{{house_type_name}}", byzs.house_type_name);
    html = html.replace("{{m2}}", byzs.m2);
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{byz_count}}", byzs.byz_count);
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{article_count}}", byzs.article_count);
    html = html.replace("{{user_id}}", byzs.user_id);
    html = html.replace("{{total_price}}", byzs.total_price);

    return html;
}

$(document).ready(function(){

    $('.diary-list-part').on('click', '.qa-desc-more', function(){
        var content = $(this).closest(".diary-content").attr("data-content");
        $(this).closest(".diary-content").html(content);
    });

    //头部条件选择
    $('.select-things').click(function(){

        var _self = $(this);
        if(!_self.hasClass("ins-info-active")){
            $(this).closest(".ins-info-select").find(".select-things").removeClass("ins-info-active");
            _self.addClass("ins-info-active");

            var share_type = $('input[name="share_type"]').val();
            var house_style = $('#c_house_style .ins-info-active').attr("data-id");
            var design_style = $('#c_design_style .ins-info-active').attr("data-id");
            var area = $('#c_area .ins-info-active').attr("data-id");
            var order = $('.list-sort .active').attr("data-order");
            var page = "1";

            init.diaryLoad(share_type, house_style, design_style, area, order, page);
        }
    });

    //内容排序切换（latest\hot）
    $('.list-sort a').click(function(){
        var _self = $(this);
        if(!_self.hasClass("active")){
            $('.list-sort a').removeClass("active");
            _self.addClass("active");

            var share_type = $('input[name="share_type"]').val();
            var house_style = $('#c_house_style .ins-info-active').attr("data-id");
            var design_style = $('#c_design_style .ins-info-active').attr("data-id");
            var area = $('#c_area .ins-info-active').attr("data-id");
            var order = $('.list-sort .active').attr("data-order");
            var page = "1";

            init.diaryLoad(share_type, house_style, design_style, area, order, page);
        }
    });

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
        var share_type = $('input[name="share_type"]').val();
        var house_style = $('#c_house_style .ins-info-active').attr("data-id");
        var design_style = $('#c_design_style .ins-info-active').attr("data-id");
        var area = $('#c_area .ins-info-active').attr("data-id");
        var order = $('.list-sort .active').attr("data-order");
        var total_page = $('input[name="total_page"]').val();

        init.diaryLoad(share_type, house_style, design_style, area, order, page);
    }
});