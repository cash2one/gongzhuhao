$(function(){	$("#save").click(function(){	//	checkFiled()		var _xsrf = $('input[name="_xsrf"]').val();		var _tip0 = $("#tip0").val();		var _tip1 = $("#tip1").val();		var _tip2 = $("#tip2").val();		var _tip3 = $("#tip3").val();		var _tip4 = $("#tip4").val();			console.log(_tip0,_tip1,_tip2,_tip3,_tip4);			$.ajax({			type:"post",			url: "/merchant/schedule/edit/template/msg/",			data: {				_xsrf:_xsrf,				tip0: _tip0,				tip1: _tip1,				tip2: _tip2,				tip3: _tip3,				tip4: _tip4			},			success: function(data){				if(data.stat == "ok"){					$("#save").attr('disable','disable');					$("#save").addClass("notAllow");	                show_dialog_reload("服务设置","保存成功");					//window.location.reload();				}else{					show_dialog_reload("服务设置",data.msg);					//alert(data.msg);				}			},				error: function(){}		});	})		//function checkFiled(){	//	if($(".tips").val() == ""){	//		alert("请填写温馨提示内容！");	//	}	//}	})