/**
 * Created by hujunhao on 14/12/9.
 */


var init = {
    projectCenterData: function(page){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/merchant/product/get",
            data: {page: page, _xsrf: _xsrf},
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;

                if(stat=="ok"){
                    $('#J-manage-project-box').html(""), $('#J-manage-page').html("");
                    var page = data.Page, totalPage = data.Total_Page, list = data.list;

                    addHtml.projectData(list);
                    totalPage !=1 ? addHtml.loadPage(page, totalPage) : "";
                }else{
                    alert(data.msg);
                }
            },
            error: function(){

            }
        });
    },
    operating: function(){
        $('#J-manage-project-box').on("click", ".project-to-delete", function(){
            var r = confirm("确认要删除这条数据吗？");
            if(r) {
                var id = $(this).attr("data-id");
                deal.deleteProjectData(id);
            }
        });
        $('#J-manage-project-box').on("click", ".project-to-sj", function(){
//            var r = confirm("确认要"+$(this).text());
//            if(r) {
                var id = $(this).attr("data-id");
                var status = $(this).attr("data-stat");
                deal.toChangeData(this, id, status);
//            }
        });
        $('input[name="toDelete"]').click(function() {
            var r = confirm("确认要删除数据吗？");
            if(r) {
                var id = "";
                $('input[name="project"]').each(function (i) {
                    if ($(this).is(":checked")) {
                        id += $(this).val() + ",";
                    }
                });
                var length = id.length;
                if (length != 0) {
                    id = id.substring(0, length - 1);
                    deal.deleteProjectData(id);
                }
            }
        });
        $('.manage-search-btn').click(function(){
            var key_word = $('input[name="manage-search-content"]').val().trim();
            key_word!=0 ? deal.toSearchData(key_word) : "";
        });
    }
}

var addHtml = {
    projectData: function(list){
        var part1, part2, part3, part4, part5;

        $.each(list, function(i){
            //序号
            var checkbox = '<input type="checkbox" name="project" class="no-checkbox" value="' + list[i].id + '">';
            //var noList = '<p class="project-No">' + list[i].id + '</p>';
            //part1 = '<div class="project-list-No" >' + checkbox + noList + '</div>';
            part1 = '<div class="project-list-No" >' + checkbox + '</div>';

            //缩略图
            var img = '<img src="'+ list[i].img_url +'" title="' + list[i].title + '" alt="">';
            var thumbnails = '<div class="project-img-show">' + img + '</div>';
            part2 = '<div class="project-list-thumbnails"><a href="/merchant/product/detail/' +list[i].id+'"  target="_blank">' + thumbnails + '</a></div>';

            //标题
            part3 = '<a href="/merchant/product/detail/' + list[i].id + '" class="project-list-title" target="_blank">' + list[i].title + '</a>';

            //上传时间
            part5 = '<div class="project-list-date"><p>' + list[i].time[0] + '</p><p>' + list[i].time[1] + '</p></div>';

             //状态
            var status = list[i].status == 0?'已上架':'未上架';
            part4 = '<p class="project-list-status">' + status + '</p>';

            //操作
            var toLook = '<a href="/merchant/product/detail/' + list[i].id + '" class="project-to-look" target="_blank">查看</a>';
            var toModify = '<a href="/merchant/product/edit/' + list[i].id + '" class="project-to-modify" target="_blank">修改</a>';
            var toDelete = '<a href="javascript:void(0)" class="project-to-delete" data-id="' + list[i].id + '">删除</a>';
            var status_opr = list[i].status == 0?'下架':'上架';
            var toStatus = '<a href="javascript:void(0)" class="project-to-sj" data-id="' + list[i].id +'"data-stat="' + list[i].status + '">'+status_opr+'</a>';
            part6 = '<div class="project-list-do clearfix">'+ toLook + toModify + toDelete + toStatus +'</div>';

            var li = '<li class="clearfix" data-id="' + list[i].id + '">'+part1+ part2 + part3 + part4 + part5 + part6+'</li>';
            $('#J-manage-project-box').append(li);
        });
    },
    loadPage: function(page, totalPage){
        $('input[name="totalPage"]').attr("value", totalPage);
        var i, pageList="", allPageList="";
        var pageHtml = {
            total: '<p class="total-page">共' + totalPage + '页</p>',
            prev: '<a href="javascript:void(0)" class="icon page-prev"></a>',
            next: '<a href="javascript:void(0)" class="icon page-next"></a>',
            point: '<p>...</p>',
            toPage: '<p class="goPage clearfix"><ins>去第</ins><input type="text" name="toPage" value=""><ins>页</ins></p>',
            btn: '<a href="javascript:void(0)" class="toJump">跳转</a>',
            activePage: '<p class="page-active">' + page + '</p>',
            page: '<a href="javascript:void(0)" class="pageNum">{{number}}</a>',
            firstPage: '<a href="javascript:void(0)" class="pageNum">1</a>',
            lastPage: '<a href="javascript:void(0)" class="pageNum">' + totalPage + '</a>'
        }

        if(totalPage<=5){
            for(i=1; i<=totalPage; i++){
                pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
            }
        }else{
            if(page<4){
                for(i=1; i<=4; i++){
                    pageList+= page==i ? pageHtml.activePage : pageHtml.page.replace("{{number}}", i);
                }
                pageList+= pageHtml.point + pageHtml.lastPage;
            }else if(page>(totalPage-4)){
                for(i=(totalPage-4); i<=totalPage; i++){
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
        }else if(page==totalPage){
            allPageList = pageHtml.prev + pageList;
        }else{
            allPageList = pageHtml.prev + pageList + pageHtml.next;
        }
        allPageList+=  pageHtml.toPage + pageHtml.btn;
        $('#J-manage-page').html(allPageList);
    }
}

var deal = {
    deleteProjectData: function(id){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/merchant/product/delete",
            data: {id: id, _xsrf: _xsrf},
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;
                var idList = id.split(",");

                if(stat=="ok"){
                    $.each(idList, function(i){
                        $('#J-manage-project-box li').each(function(){
                            if($(this).attr("data-id")==idList[i]){
                                $(this).remove();
                            }
                        });
                    });
                    if($('input[name="totalPage"]').val()!=1){
                        if($('#J-manage-project-box li').length==0){
                            $('input[name="projectCheck"]').prop("checked", false);
                            var page = parseInt($('input[name="page"]').val()) - ($('input[name="page"]').val() == $('input[name="totalPage"]').val() ? 1 : 0);
                            init.projectCenterData(page);
                        }
                    }
                }else{
                    alert(data.msg);
                }
            },
            error: function(){

            }
        });
    },
    toSearchData: function(key_word){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/merchant/product/select",
            data: {key_word: key_word, _xsrf: _xsrf},
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;

                if(stat=="ok"){
                    $('#J-manage-project-box').html(""), $('#J-manage-page').html("");
                    var page = data.Page, totalPage = data.Total_Page, list = data.list;

                    addHtml.projectData(list);
                    totalPage !=1 ? addHtml.loadPage(page, totalPage) : "";
                }else{
                    alert(data.msg);
                }
            },
            error: function(){

            }
        });
    },
     toChangeData: function(_this, id, status){
        var _xsrf = $('input[name="_xsrf"]').val();

        jQuery.ajax({
            type: "POST",
            url: "/merchant/product/publish",
            data: {id: id, status:status, _xsrf: _xsrf},
            dataType: "JSON",
            success: function(data){
                var stat = data.stat;

                if(stat=="ok"){
                    alert($(_this).text()+'成功！')
                    if (parseInt(status) == 0){
                        $(_this).attr('data-stat', 1);
                        $(_this).text('上架');
                        $(_this).parent().siblings('.project-list-status').text('未上架');
                    }else if  (parseInt(status) == 1){
                        $(_this).attr('data-stat', 0);
                        $(_this).text('下架');
                        $(_this).parent().siblings('.project-list-status').text('已上架');
                    }
                    else{
                        alert('数据错误！');
                        window.location.reload(true);
                    }
                }else{
                    alert(data.msg);
                }
            },
            error: function(){

            }
        });
    }
}


$(document).ready(function(){

    //所有项目的全选和取消全选
    $("input[name='projectCheck']").click(function(){
        $('input[name="project"]').prop("checked", $(this).is(":checked"));
    });
    $('#J-manage-project-box').on("click", ".no-checkbox", function(){
        var allChecked = true;
        $('.no-checkbox').each(function(){
            if(!$(this).is(":checked")){
                allChecked = false;
            }
        });
        $('input[name="projectCheck"]').prop("checked", allChecked);
    });

    //翻页方法在此
    $('#J-manage-page').on("click", ".pageNum", function(){
        var page = $(this).text();
        $('input[name="page"]').attr("value", page);
        init.projectCenterData(page);
    });
    $('#J-manage-page').on("click", ".page-prev", function(){
        var page = parseInt($('input[name="page"]').val())-1;
        $('input[name="page"]').attr("value", page);
        init.projectCenterData(page);
    });
    $('#J-manage-page').on("click", ".page-next", function(){
        var page = parseInt($('input[name="page"]').val())+1;
        $('input[name="page"]').attr("value", page);
        init.projectCenterData(page);
    });
    $('#J-manage-page').on("click", ".toJump", function(){
        var page = parseInt($('input[name="toPage"]').val());
        var totalPage = parseInt($('input[name="totalPage"]').val());
        if(page<=totalPage){
            $('input[name="page"]').attr("value", page);
            init.projectCenterData(page);
        }else{
            alert("请输入正确页数！");
            $('input[name="toPage"]').attr("value", "");
        }
    });
});