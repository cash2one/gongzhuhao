$(function(){
	$("#nav a:first,#con div:first").addClass("on");
	$("#nav a").each(function(i){
		$(this).click(function(){
			$(this).addClass("on").parent().siblings().find("a").removeClass("on");
			$($("#con div")[i]).show().siblings().hide();
		});
	});	
})
