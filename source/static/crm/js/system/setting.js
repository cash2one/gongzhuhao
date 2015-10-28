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
	
	$("#js_save_x").click(function(e){
		
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
	
		$.ajax({
			type:"post",
			url:"/merchant/system/edit/shareextendinfo/",
			data: {
				_xsrf:_xsrf,
				Finfo: _info,
	            Fid: _id,
			},
			success: function(data){
				if(data.stat == "ok"){
					$("#js_save_x").attr('disable','disable');
					$("#js_save_x").addClass("notAllow");
	                show_dialog_reload("服务设置","保存成功");
					//window.location.href = "/merchant/system/edit/shareextendinfo/";
				}else{
					show_dialog_reload("服务设置",data.msg);
				}
			},
	
			error: function(){
			}
		});
	})
	
	$("#js_cancel_x").click(function(){
		window.location.href = "/merchant/system/edit/shareextendinfo/";
	})


	
})
