$(function(){
	
	//添加员工
	$("#js_staffer_add").click(function(){
		checkForm();
		var _staff_depart = $("#staff-derapt option:selected").val();
		var _staff_name = $("#staff-name").val();
		var _staff_email = $("#staff-email").val();
		var _staff_mobile = $("#staff-mobile").val();
		var _staff_title = $("#staff-title option:selected").val();
		var staff_id = $("#m-staff-id").val();
		var _xsrf = $('input[name="_xsrf"]').val();
		
		$.ajax({
			type:'POST',
			url:'/merchant/staffers/edit/'+staff_id+'/',
			data: {
				_xsrf:_xsrf,
				dpt_id:_staff_depart,
				name: _staff_name,
				mobi: _staff_mobile,
				email: _staff_email,
				title: _staff_title
			},
			success:function(data){
				if(data.stat == 'ok'){
					$("#js_staffer_add").attr('disable','disable');
					$("#js_staffer_add").addClass("notAllow");
					$("#input-txt").attr("value","");
					$('#addMemModal').hide();
					window.location.reload();
				}else{
					alert(data.msg);
				}	
			},
			error: function(){
				
			}
		})
	})
	
	//编辑员工
	$("#js_staffer_edit").click(function(){
		checkForm();
		var _staff_depart = $("#staff-derapt-m option:selected").val();
		var _staff_name = $("#staffer-name-m").val();
		var _staff_email = $("#staffer-email-m").val();
		var _staff_mobile = $("#staffer-mobile-m").val();
		var _xsrf = $('input[name="_xsrf"]').val();
		var _staff_id = $("#staff-id").val();
		
		
		$.ajax({
			type: 'POST',
			url:'/merchant/staffers/edit/' + _staff_id + "/",
			data: {
				dpt_id:_staff_depart,
				name: _staff_name,
				//title: _staff_title,
				mobi: _staff_mobile,
				email: _staff_email,
				_xsrf:_xsrf
			},
			success:function(data){
				if(data.stat === 'ok'){
					$("#js_staffer_edit").attr('disable','disable');
					$("#js_staffer_edit").addClass("notAllow");
					alert("修改成功！");
					window.location.href = "/merchant/departments/" + _staff_depart;
				}else{
					alert(data.msg);
				}	
			}
		})
	})	
	
	//删除员工
	$(".member-list").on('click','.btn-del',function(){
		var _staff_id = $(this).attr('data-id');
		var _xsrf = $('input[name="_xsrf"]').val();
		var _html = $(".btn-del").parent().parent();
		
	    BootstrapDialog.show({
            title: '删除员工',
            message: '确定删除员工',
            buttons: [{
                label: 'Cancle',
                action: function(dialogItself){
                    dialogItself.close()
                }
            },
            {
                label: 'OK',
                action: function(dialogItself){
                    dialogItself.close()
					$.ajax({
						type:"post",
						url:"/merchant/staffers/delete/" + _staff_id + "/",
						data:{
							_xsrf:_xsrf
						},
						success:function(data){
							var obj = $.parseJSON(data);
							show_dialog_reload('删除员工',obj.info);
							if(obj.status=='ok'){

								_html.remove();
								//window.location.reload();
							}
						},
						error: function(){
							
						}
					})		                    
                 }
                      
                      
                }]
           })
        });	
	//删除员工
//	$(".btn-del").click(function(){
//		var _staff_id = $(this).attr('data-id');
//		var _xsrf = $('input[name="_xsrf"]').val();
//		console.log(_staff_id);
//		
//		if(confirm("确认要删除？")){
//			var _html = $(this).parent().parent();
//			$.ajax({
//				type:"post",
//				url:"/merchant/staffers/delete/" + _staff_id + "/",
//				data:{
//					_xsrf:_xsrf
//				},
//				success:function(data){
//					if(data.stat == 'ok'){
//						
//						_html.remove();
//					}else{
//						alert(data.msg);
//					}
//				},
//				error: function(){
//					
//				}
//			})		
//		}
//	})
	
	$("#js_staffer_cancel").click(function(){
		window.location.href = "/merchant/staffers/"
	})
	
})
function checkForm(e){
    if($("#staff-name").val() == ""){
        $("#staff-name").after('<div class="error">姓名不能为空</div>');
        $("#staff-name").focus();
        e.preventDefault();
        return false;
    }

	if($("#staff-mobile").val() == ""){
		$("#staff-mobile").after('<div class="error">手机号码不能为空</div>');
		$("#staff-mobile").focus();
		e.preventDefault();
		return false;
	}

}
