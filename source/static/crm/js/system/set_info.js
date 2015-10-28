$(function(){
		//字数统计
    $("#description").keyup(function(){
        var _curLength = $("#description").val().length;
        if(_curLength > 50){
            var _num = $("#description").val().substr(0, 50);
            $("#description").val(_num);
        }else{
          /*$("#txt-count").text($("#description").val().length + '/300')*/
         	$("#txt-count").text("最多输入50字，您已输入：" + $("#description").val().length);
        }
    });	
    
	var _html = $("#js_setting").find(".error");

	$(".form-control").keyup(function(){
		_html.html("");
	    $(this).css("border","1px solid #4cc25c");
	});
	
	$(".form-control").blur(function(){
		_html.html("");
	    $(this).css("border","1px solid #d8d8d8");
	});
	
	$("#js_save_p").click(function(e){
		 
		if($("#description").val() == ""){
			$("#description").focus().css("border","1px solid #f00");
			$(".info-error").html("信息不能为空");
			e.preventDefault();
			return false;
		}			
		
		_html.html("");
	    $(this).css("border","1px solid #d8d8d8");	
	
		var _xsrf = $('input[name="_xsrf"]').val();
		var _info = $("#description").val();
		var _id = $("#Fid").val();
		
		//console.log(_info);
	
		$.ajax({
			type:"post",
			url:"/merchant/system/edit/shareprizeinfo/",
			data: {
				_xsrf:_xsrf,
				Finfo: _info,
	            Fid: _id,
			},
			success: function(data){
				if(data.stat == "ok"){
					$("#js_save_p").attr('disable','disable');
					$("#js_save_p").addClass("notAllow");
					show_dialog_reload("分享设置","设置成功！");
					//window.location.href = "/merchant/system/edit/shareprizeinfo/";
				}else{
					show_dialog_reload("分享设置",data.msg);
				}
			},
	
			error: function(){
			}
		});
	})	
	

	$("#js_cancel_p").click(function(){
		window.location.href = "/merchant/system/edit/shareprizeinfo/";
	})	
})
