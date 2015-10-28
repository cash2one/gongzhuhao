/**
 * Created by jane on 15/5/29.
 */
$(function(){

    //滑动固定导航头操作
    $(".topic-item-nav").stick_in_parent({"offset_top":44});

    
    var _tid = $("#topic_category_id").val();
    var _num = $("#type_num").val();

    var page_code = 2 ,
        basepath = "/mobile/topics/query/"+_tid+"/"+_num+"/";

    $(".btn-more").click(function(e){
        var url = basepath + page_code;
        var promise = $.get(url);
        promise.success(function(rs){
            rs = JSON.parse(rs);
            if(rs.has_next == 1){
                page_code += 1;
                $('.btn-more').show();
            }else{
                $(".btn-more").hide();
            }
            $('.topic-lists').append(rs.html);
        });

        promise.error(function(error){
            console.log(error);
        });
    });
});