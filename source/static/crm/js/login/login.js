/*
 * Author: zjgoing@gmail.com
 * Date: 2015-01-21
 * Func: login js
 */
$(function(){
	
	var _html = $(this).closest("＃login-box").find(".error");
	
	//输入区域输入状态下错误提示消失，文本框颜色改变
	$(".input-txt").keyup(function(){
		_html.html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	$(".input-txt").blur(function(){
		_html.html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
})
