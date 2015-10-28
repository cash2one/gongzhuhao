$(function(){
	/*侧推 开始*/
	var pushStatus = 0;
    $('.btn-menu').click(function(){
		if(pushStatus == 0){
			$('.aside-menu').addClass('aside-show').removeClass('aside-hide');
			$('.be-pushed').addClass('push-out').removeClass('push-back');
			pushStatus = 1;
		}else if(pushStatus == 1){
			$('.aside-menu').addClass('aside-hide').removeClass('aside-show');
			$('.be-pushed').addClass('push-back').removeClass('push-out');
			pushStatus = 0;
		}
	});
	
	$('.case-list-nav a').click(function(){
		$(this).addClass('current').siblings().removeClass('current');
	});
});