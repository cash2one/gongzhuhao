/**
 * Created by jane on 15/5/30.
 */
$(function(){

    var _tid = $("#topic_id").val();
    // var _num = $("#type_num").val();

    var page_code = 2 ,
        basepath = "/mobile/topic/detail/"+_tid+"/";

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
            $('.posts-reply-item').append(rs.html);
        });

        promise.error(function(error){
            console.log(error);
        });
    });
});