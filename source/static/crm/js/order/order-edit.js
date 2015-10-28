$(function(){
	$(".order-date span").on({
		mouseenter: function(){
			$(this).parent().find(".showInfos").show();
		},
		mouseleave: function(){
			$(this).parent().find(".showInfos").hide();
		}
	})

    $(".bride.hide-this").hide();
    $(".customer-name").empty().html('客户名称<em class="red">*</em>');

	$(".type-bdrde").click(function(){
		$(this).attr("checked","true");
		$(".bride").show();
		$(".customer-name").empty().html('新娘<em class="red">*</em>');
	});
	
	$(".type-other").click(function(){
		$(this).attr("checked","true");
		$(".bride").hide();
		$(".customer-name").empty().html('客户名称<em class="red">*</em>');
	});

	var _tipHtml = $(".save").closest(".modal").find(".error");
	
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

	$('.datatime').datetimepicker({
		lang:'ch',
		timepicker:false,
		format:'Y-m-d',
		formatDate:'Y-m-d',
		scrollInput:false,
		validateOnBlur:false
	});

	//检测修改订单必填的选项
	function checkInputM(event){
		if($("#m_user_name").val() == ""){
			_tipHtml.html("用户名不能为空");
			$("#m_user_name").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}
		if($("#m_user_mobi").val() == ""){
			_tipHtml.html("手机号码不能为空");
			$("#m_user_mobi").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}
		if($("#m_order-num").val() == ""){
			_tipHtml.html("订单号码不能为空");
			$("#m_order-num").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}
		if($("#m_order_amount").val() == ""){
			_tipHtml.html("订单金额不能为空");
			$("#m_order_amount").focus().css("border","1px solid #f00");
			event.preventDefault();
			return false;
		}		
	}
	
	
	//修改订单
	$("#js_save").click(function(){
//		checkInputM();
		var _order_id = $("#order_id_m").val();	
		var _xsrf = $('input[name="_xsrf"]').val();
		var _order_type = $('input[name="type"]:checked').val();
		var _user_name = $("#m_user_name").val();
		var _user_mobi = $("#m_user_mobi").val();
		var _user_birth = $("#m_user_birth").val();
		var _user_name_ex = $("#m_user_name_ex").val();
		var _user_mobi_ex = $("#m_user_mobi_ex").val();
		var _user_birth_ex = $("#m_user_birth_ex").val();
		var _order_id_user = $("#m_order_num").val();
		var _amount = $("#m_order_amount").val();
		var p_amount = $("#pre_order_amount").val();
		var retainage = '';
		$('input[name="retainage"]').each(function() {
          retainage+=$(this).val()+','
        });

		//var _uid_stf = $("#m_order_stf").text();
		var create_time = $('#create_time').val()
		var _uid_stf = $("#m_order_stf").attr('value');
	    var orders_from = '';
        $("input[name='order_from']:checked").each(function(){
            orders_from+= $(this).val()+',';
        });
		var _comment = $("#m_order_comment").val();
        if(!_uid_stf){
            _uid_stf = 0;
        }
        $.ajax({
            type:"post",
            url:"/merchant/orders/update/"+_order_id+"/",
            data:{
                order_id:_order_id,
                _xsrf:_xsrf,
                order_type:_order_type,
                user_name:_user_name,
                user_mobi:_user_mobi,
                user_birth:_user_birth,
                user_name_ex:_user_name_ex,
                user_mobi_ex:_user_mobi_ex,
                user_birth_ex:_user_birth_ex,
                order_id_user:_order_id_user,
                orders_from:orders_from,
                amount:_amount,
                create_time:create_time,
                pre_order_amount:p_amount,
                uid_stf:_uid_stf,
                comment:_comment,
                retainage:retainage
            },
            success:function(data){
                var obj = $.parseJSON(data);
                if(obj.stat == 'ok'){
					$("#js_save").attr('disable','disable');
					$("#js_save").addClass("notAllow");
                    show_dialog_location_href('新增订单','保存成功','/merchant/orders/list/7');
                }else{
                    show_dialog_none_reload('新增订单',obj.msg)
                }
            },
            error:function(){}
        });

	});

	$("#cancel").click(function(){
		window.location.href = "/merchant/orders/list/7"
	})
})



