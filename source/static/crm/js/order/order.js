$(function(){
	$('.datatime').datetimepicker({
	    lang:'ch',
		timepicker:false,
		format:'Y-m-d',
		scrollInput:false,
		validateOnBlur:false
	});
	
	$(".state span").on({
		mouseenter: function(){
			$(this).parent().find(".showInfos").show();
		},
		mouseleave: function(){
			$(this).parent().find(".showInfos").hide();
		}
	})
	
	$(".type-bdrde").click(function(){
		$(".bride").show();
		$(".customer-name").empty().html('新娘<em class="red">*</em>');
	});
	
	$(".type-other").click(function(){
		$(".bride").hide();
		$(".customer-name").empty().html('客户名称<em class="red">*</em>');
	});
	
	var _tipHtml = $(".save").closest(".order-edit").find(".error");
	
	$(".form-control").keyup(function(){
		_tipHtml.html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	$(".form-control").blur(function(){
		_tipHtml.html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
	$(".save").click(function(){
		_tipHtml.html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});	
	
	//检测添加订单必填的选项
	function checkInput(event){
		if($("#user_name").val() == ""){
			_tipHtml.html("用户名不能为空");
			$("#user_name").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}

		if($("#order_amount").val() == ""){
			_tipHtml.html("订单金额不能为空");
			$("#order_amount").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}	
		if($("#order_amount").val() == ""){
			_tipHtml.html("备注不能为空");
			$("#m_order_comment").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}
	}

	//添加订单
	$("#save-stf").on('click',function(e){
		checkInput();
		var _order_id = $("#order_id").val();
		var _order_no = $("#order-no").val();
		var _order_type = $('input[name="type"]:checked').val();
		var _order_num = $("#order_num").val();
		var _user_name = $("#user_name").val();
		var _user_mobi = $("#user_mobi").val();
		var _user_birth = $("#user_birth").val();
		var _user_name_ex = $("#user_name_ex").val();
		var _user_mobi_ex = $("#user_mobi_ex").val();
		var _user_bitrh_ex = $("#user_birth_ex").val();
		var _order_amount = $("#order_amount").val();
		var _user_stf = $("#m_order_stf").attr('value');
		var _order_desc = $("#order_comment").val();
		var _pre_order_amount = $("#pre_order_amount").val();
		var create_time = $('#create_time').val()
		var orders_from = '';
        $("input[name='order_from']:checked").each(function(){
            orders_from+= $(this).val()+',';
        });
		var _xsrf = $('input[name="_xsrf"]').val();
        if(!_user_stf){
            _user_stf = 0;
        }
        $.post("/merchant/orders/add/",{
                        order_id_user: _order_num,
                        order_type: _order_type,
                        user_name: _user_name,
                        user_mobi: _user_mobi,
                        user_birth: _user_birth,
                        user_name_ex: _user_name_ex,
                        user_mobi_ex: _user_mobi_ex,
                        user_birth_ex: _user_bitrh_ex,
                        amount: _order_amount,
                        uid_stf: _user_stf,
                        pre_order_amount:_pre_order_amount,
                        orders_from:orders_from,
                        create_time:create_time,
                        comment: _order_desc,
                        _xsrf:_xsrf
                },function(json_data){
                    var data = $.parseJSON(json_data);
                    if(data.stat == "ok"){
						$("#save-stf").attr('disable','disable');
						$("#save-stf").addClass("notAllow");
                         window.location.href="/merchant/orders/list/7";
                         //show_dialog_location_href('添加订单','保存成功',"/merchant/orders/list/7");
                    }else{
                        $("#save-stf").removeAttr('disable');
                        show_dialog_none_reload("添加订单",data.msg);
                    }
				});

	});
	
	
	//弹出二维码层
	$("#order-all .btn-share").click(function(){
		var _this = $(this);
		$(this).closest(".order-action").find(".shareQR").css("display","inline-block");
		var _dialog = $(this).closest("#order-all").find(".order-action").find(".dialog");
		var _close = _dialog.find(".close");
		_close.click(function(){
			$(_dialog).parent().css('display','none')
		});
	});
	
})



