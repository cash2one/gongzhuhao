$(function(){	
	//删除套系
	$(".sortable").on('click','.delete',function(){
		var _series_id =  $(this).attr('data-id');
		var _xsrf = $('input[name="_xsrf"]').val();
		var _html = $(this).parent().parent();

	    BootstrapDialog.show({
            title: '删除套系',
            message: '确定删除套系？',
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
						type:"get",
						url:"/merchant/series/delete/" + _series_id + "/",
						data:{
							_xsrf:_xsrf
						},
						success:function(data){
							//var obj = $.parseJSON(data);
							_html.remove();
							if(data.stat == 'ok'){
								$(".sortable").attr('disable','disable');
								$(".sortable").addClass("notAllow");
								show_dialog_reload('删除套系','删除套系成功');
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
})

