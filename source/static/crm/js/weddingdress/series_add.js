$(function(){
	//输入区域输入状态下错误提示消失，文本框颜色改变
	$(".form-control").keyup(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #4cc25c");	
	});	
	$(".form-control").blur(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
	
	$(".add").on("click",function(){
		//var _html = '<input type="text" class="form-control input-write" />';
		$(this).before("<input type='text' class='form-control input-write' />");
	});
	
	$("#save").on("click",function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");
	    if (!checkForm())
	        return;
	   
	    var _package_name = $("#package-name").val();  //套系名称
	    var _price = $("#price").val();  //原价
	    var _sale_price = $("#sale-price").val();  //现价
	    var _type = $("input[name='type']:checked").val();  //套餐形式
	    var _freetrial = $("input[name='freetrial']:checked").val();  //0元试纱
	    var _count = $("#count").val();  //服装数量
	    var _description = $("#description").val();  //类型说明
	    var _extra = $("#extra").val();  //补充说明
	    


	    var _promise = $("input[name='promise']:checked").val();//商户承若
	    var _statement = $("input[name='statement']:checked").val();//商户信息发布声明
	    
	    var _cover_id = $("#cover").attr("data-id"); //封面图ID
		var _cover_url = $("#cover").attr("src");//封面图URL
	    
		var _works_info = new Object(); //上传作品的图片ID以及描述信息
		var _index = 0;
		$(".photo-item").each(function(){
			var imgItem = new Object();
			imgItem["id"] = $(this).find("img").attr("data-id");
			imgItem["desc"] = $(this).find("textarea").val();
			_works_info[_index] = imgItem;
			_index++;
		});
		var images = JSON.stringify(_works_info);	    
		

	    var _xsrf = $('input[name="_xsrf"]').val();
	    var _post_url = $('input[name="post_url"]').val();

		$.ajax({
			type:"post",
			url: _post_url,
			dataType: 'JSON',
			data:{
				package_name:_package_name,
				price: _price,
				sale_price: _sale_price,
				type: _type,
				freetrial: _freetrial,
				count: _count,
				description: _description,
				extra: _extra,
				promise: _promise,
				statement: _statement,
				_xsrf: _xsrf,
				cover_img:_cover_url,
				images:images
			},
			success:function(data){
				if(data.stat == 'ok'){
					$("#save").attr('disable','disable');
					$("#save").addClass("notAllow");
					show_dialog_reload("套系发布","发布成功");
					window.location.href = "/merchant/weddingdress/series/list/";
				}else{
					show_dialog_reload("套系发布",data.info);
					//alert(data.info);
				}

			},
			error: function(){
				
			}
		});
		
	})

	//删除图片
	$(".photo-thumb").on('click','.delete-photo', function(){
		var _html = $(this).parent();

		if(confirm("确定要删除吗？")){
		     var work_img_id = $(this).parent().find("img").attr('data-id');
		     $.get("/merchant/weddingdress/series/delete/img/"+work_img_id,{},function(data){
		     	if(data.stat == 'ok'){
		            _html.remove();
		        }else{
		           show_dialog_reload('删除失败');
		        }
		     }, 'JSON')
			return false;
		}
	});

})

$(document).ready(function() {
	//上传封面图
	 $("#coverupload").click(function(){
	 	var uploader = $("#js_cover");
	 	addCover(uploader);
	 })
	 
	function addCover(uploader, i) {
	    uploader.fileupload({
	        dataType: 'json',
	        autoUpload: true,
	        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	        //maxNumberOfFiles : 10,
	        maxFileSize: 5000000,
	        done: function (e, data) {
		        	$.each(data.result.files, function (index, file) {
	                $("#cover").attr("src", file.url);
	                $("#cover").attr("data-id", file.id);
	            });
	        },
	        send: function (e, data) {
//	            var _html = '<img class="cover" id="cover" src="" data-id="" alt="" title="封面图" />';
//	            $("#coverupload").before(_html)
				$("#cover").attr("src", "/static/crm/js/plugins/uploadify/img/user-loading.gif");
	        }
	    });
	    uploader.find("input:file").removeAttr('disabled');
	}		
	
	
	//上传图片
	$('#fileupload').click(function () {
	    var uploader = $("#J-formFile");
	    var i = $('#J-append-photo li').length;
	    addPhoto(uploader, i);
	});

	function addPhoto(uploader, i) {
	    uploader.fileupload({
	        dataType: 'json',
	        autoUpload: true,
	        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	        maxFileSize: 5000000,
	        done: function (e, data) {
	            $.each(data.result.files, function (index, file) {
	                //$('#J-append-photo li:eq(' + i + ')').attr("data-id", file.id);
	                $('#J-append-photo li:eq(' + i + ')').attr("sort-id", i);
	                $('#J-append-photo li:eq(' + i + ')').find("img").attr("src", file.url);
	                $('#J-append-photo li:eq(' + i + ')').find("img").attr("data-id", file.id);
	                i++;
	            });
	        },
	        send: function (e, data) {
	            var html = $('#J-model-photo').html();
//	            $('#js-photo').after(html);
				$("#J-append-photo").append(html);
	        }
	    });
	    uploader.find("input:file").removeAttr('disabled');
	}		
});

function checkForm(e){
	if($("#package-name").val() == ""){
		$(".package-error").html("请填写套系名称！");
		$("#package-name").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#price").val() == ""){
		$(".price-error").html("请填写原价");
		$("#price").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#sale-price").val() == ""){
		$(".sale-price-error").html("请填写现价");
		$("#sale-price").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#count").val() == ""){
		$(".count-error").html("请填写衣服数量");
		$("#count").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#description").val() == ""){
		$(".description-error").html("请描述婚纱的类型(分隔符为、)");
		$("#descriptiont").focus().css("border","1px solid #f00");
		return false;
	}

	if($("input[name='promise']:checked").length < 0){
		alert("请选择商户承若！");
		return false;
	}
	
	if($("input[name='promise']:checked").length < 0){
		alert("请选择《商户信息发布声明》！");
		return false;
	}
	return true;
}