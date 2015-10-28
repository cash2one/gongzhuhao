$(function(){
	$('#add').click(function(event){
		if($("#dpt_name").val() == ""){
			$("#dpt_name").focus().css("border","1px solid #f00");
			$(".dpt-eror").html("请填写部门名称！");
			event.preventDefault();
		}
		
		
		var _dpt_pre_id = $('#dpt_pre_id option:selected').val();
		var _dpt_name = $('#dpt_name').val();
		var _xsrf = $('input[name="_xsrf"]').val();
		$.ajax({
			type:"POST",
			url:"/merchant/departments/add/",
			//async:true,
			data:{
				dpt_pre_id:_dpt_pre_id,
				dpt_name: _dpt_name,
				_xsrf:_xsrf
			},
			success:function(data){
				$('#dpt_name').val('');
				if(data.stat === 'ok'){
					//alert(rsp.msg);
					$("#add").attr('disable','disable');
					$("#add").addClass("notAllow");
					window.location.reload();
				}else{
					alert(data.msg);	
				}
				
			}
		});
	
	})

})
