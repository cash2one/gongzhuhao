/**
 * Created by hujunhao on 14/12/4.
 * modify by hujunhao on 15/1/29
 */


$(document).ready(function(){

    //店铺分店和地址的更多显示和隐藏
    $('.show-all').click(function(){
        $(this).closest('.all-info').find('.info-more-layer').slideToggle();
    });
    $('.close').click(function(){
        $(this).closest('.info-more-layer').slideUp();
    });

    //缩略图到大图的切换
    $('.merchant-result-box').on("click", '.thumbnails', function () {
        var _self = $(this);
        var src = _self.attr("data-src");
        _self.closest("li").find(".choice-case img").attr("src", src);
    });

    $('.owner-share-tab a').click(function(){
        var _self = $(this);

        if(!_self.hasClass("os-active")){
            $('.owner-share-tab a').removeClass("os-active");
            _self.addClass("os-active");
            if(_self.hasClass("o-diary")){
                $('#J-os_share_photo').hide();
                $('#J-os_share_diary').show();
            }else{
                $('#J-os_share_diary').hide();
                $('#J-os_share_photo').show();
            }
        }
    });
});