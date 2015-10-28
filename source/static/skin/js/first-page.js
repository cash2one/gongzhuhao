/**
 * Created by hujunhao on 15/4/22.
 */

var init = {
    addProject: function(step, area, qu, page){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/project",
            data: {
                current_qu_id:qu,
                current_stage_id:step,
                current_m2_id:area,
                page: page,
                _xsrf: _xsrf
            },
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;

                if(stat=="ok"){
                    $('.m-pro-list').empty();
                    var list = data.all_projects,
                        page = data.page,
                        total_page = data.total_page;

                    if(list.length>0) {
                        $.each(list, function (i) {
                            var html = $('#J-model-project').html();
                            var templates = toReplaceModel(html, list[i]);

                            $('.m-pro-list').append(templates);
                        });
                    }
                    parseInt(total_page) > 1 ? init.loadPage(page, total_page) : $('#J-manage-page').empty();

                }else{
                    alert(data.msg);
                }
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

/* 模板加载需先加载空模板 */
function toReplaceModel(html, list){
    html = html.replace("{{owner_user_id}}", list.owner_user_id);
    html = html.replace("{{photo}}", list.photo);
    html = html.replace("{{owner_user_id}}", list.owner_user_id);
    html = html.replace("{{nick}}", list.nick);
    html = html.replace("{{design_for_display}}", list.design_for_display);
    html = html.replace("{{all_address}}", list.all_address);
    html = html.replace("{{gmt_created}}", list.gmt_created);
    html = html.replace("{{stage_name}}", list.stage_name);

    if(list.last_modified_time==""){
        html = html.replace("{{date}}", '暂无汇报');
    }else {
        html = html.replace("{{date}}", '最后汇报：' + list.last_modified_time + ' | ' + list.progress_count + ' 次');
    }

    if(list.is_display_article){
        html = html.replace("{{is_display_article}}", '<a href="/member/decorate_article/edit/' + list.owner_user_id + '" class="m-pro-lookDiary" target="_blank">查看直播</a>');
    }else{
        html = html.replace("{{is_display_article}}", '<p class="m-pro-noDiary">暂无日记</p>');
    }

    html = html.replace("{{project_id}}", list.project_id);
    html = html.replace("{{project_id}}", list.project_id);
    html = html.replace("{{visit_slogan}}", list.company.visit_slogan);
    html = html.replace("{{order_slogan}}", list.company.order_slogan);
    html = html.replace("{{company_name}}", list.company_name);

    html = html.replace("{{company_name}}", list.company_name);

    return html;
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
    var qu = $('#c_qu .ins-info-active').attr("data-id");
    var step = $('#c_design_style .ins-info-active').attr("data-id");
    var area = $('#c_area .ins-info-active').attr("data-id");

    init.addProject(step, area, qu, page);
}

$('.select-things').click(function(){
    var _self = $(this);
    if(!_self.hasClass('ins-info-active')) {
        _self.closest("li").find('.select-things').each(function () {
            $(this).removeClass('ins-info-active');
        });
        _self.addClass('ins-info-active');

        var step = $('#c_design_style .ins-info-active').attr('data-id'),
            area = $('#c_area .ins-info-active').attr('data-id'),
            qu = $('#c_qu .ins-info-active').attr('data-id'),
            page = 1;
        init.addProject(step, area, qu, page);
    }
});