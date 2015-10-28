/**
 * Created by jane on 15/6/5.
 */
$(function(){

    //个人中心Tab功能
	$("#js_tab li:first,#js_tabCon .tab-con:first").addClass("on");
		$("#js_tab li").each(function(i){
		$(this).click(function(){
			$(this).addClass("on").siblings().removeClass("on");
			$($("#js_tabCon .tab-con")[i]).show().siblings().hide();
		});
	});

    //个人中心导航显示与隐藏
    $(".gzh-header-nav").hover(function(){
        $(this).find(".gzh-nav").show();
        return false;
    },function(){
        $(this).find(".gzh-nav").hide();
    });

})