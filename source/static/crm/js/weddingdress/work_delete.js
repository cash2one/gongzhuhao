$(function(){    
	$(".work").on('click','.delete',function(){
		var _work_id = $(this).attr('data-id');
		var _xsrf = $('input[name="_xsrf"]').val();
		var _html = $(this).parent().parent();

	    BootstrapDialog.show({
            title: '删除作品',
            message: '确定删除作品？',
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
						url:"/merchant/weddingdress/work/delete/" + _work_id,
						data:{
							_xsrf:_xsrf
						},
						success:function(data){
							//var obj = $.parseJSON(data);
							_html.remove();
							
							if(data.stat == 'ok'){
								show_dialog_reload('删除作品','删除作品成功');
								window.location.reload();
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
