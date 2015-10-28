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
	   
	    var _package_name = $("#package-name").val();//套系名称
	    var _price = $("#price").val();//原价
	    var _sale_price = $("#sale-price").val();//现价
	    var _bride_style_count = $("#bride-style-count").val();//新娘造型
	    var _groom_style_count = $("#groom-style-count").val();//新郎造型
	    var _cloth_select_type = $("input[name='cloth_select_type']:checked").val();//服装选择
	    var _cloth_remark = $("#cloth-remark").val();//补充说明
	    
	    var _outdoor_space="";  //外景地
    		$("#outdoor .input-write").each(function(){
                if($(this).val()!='')
                _outdoor_space += $(this).val() + ";";
    		})  
	    
	    var _inner_space = ""; //内景地
	    $("#inner .input-write").each(function(){
               if($(this).val()!='')
                _inner_space += $(this).val() + ";";
    		})  
	    
	    var _space_remark = $("#space-remark").val();// 补充说明
	    var _shot_desc = $("#shot-desc").val(); //套系特色
	    var _photographer_level = $("#photographer-level").val(); //摄影师级别
	    
	   	var _recommend_photographer = ""; //推荐摄影师
	    $("#photographer .input-write").each(function(){
               if($(this).val()!='')
                _recommend_photographer += $(this).val() + ";";
    		})  
    		
	   	var _arter_level = $("#arter-level").val(); // 化妆师级别
	   	var _recommend_arter = ""; //推荐化妆师
	    $("#arter .input-write").each(function(){
	        if($(this).val()!='')
     		    _recommend_arter += $(this).val() + ";";
    		})  
    		
	    var _photo_album_desc = $("#photo-album-desc").val(); //相册
	    var _photo_frame_desc = $("#photo-frame-desc").val(); //相框
	    var _mv_desc = $("#mv-desc").val(); //MV
	    var _other_desc = $("#other-desc").val();//其他
	    
	    var _description = $("#description").val();//其他补充说明
	    var _other_pay = $("#other-pay-desc").val();//其他收费项目
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
		
		console.log(images);
	    
	    var _xsrf = $('input[name="_xsrf"]').val();
		var _series_id = $("#series-id").val();//套系ID
		
		$.ajax({
			type:"post",
			url:"/merchant/series/add/" + _series_id + "/",
			dataType: 'JSON',
			data:{
				package_name:_package_name,
				price: _price,
				sale_price: _sale_price,
				bride_style_count: _bride_style_count,
				groom_style_count: _groom_style_count,
				cloth_select_type: _cloth_select_type,
				cloth_remark: _cloth_remark,
				outdoor_space: _outdoor_space,
				inner_space: _inner_space,
				space_remark: _space_remark,
				shot_desc: _shot_desc,
				photographer_level: _photographer_level,
				recommend_photographer: _recommend_photographer,
				arter_level: _arter_level,
				recommend_arter: _recommend_arter,
				photo_album_desc: _photo_album_desc,
				photo_frame_desc: _photo_frame_desc,
				mv_desc: _mv_desc,
				other_desc: _other_desc,
				description: _description,
				other_pay:_other_pay,
				promise: _promise,
				statement: _statement,
				_xsrf: _xsrf,
				cover_url:_cover_url,
				images:images
			},
			success:function(data){
				if(data.stat == 'ok'){
					$("#save").attr('disable','disable');
					$("#save").addClass("notAllow");
					show_dialog_reload("套系发布","发布成功");
					window.location.href = "/merchant/series/";
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
		     work_img_id = $(this).attr('data-id');
		     $.get('/merchant/series/delete/img/'+work_img_id,{},function(data){
		        //alert(data);
		        if(data=='ok'){
		            _html.remove();
		        }else{
		           alert('删除失败');
		        }
		     })
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
	
	if($("#bride-style-count").val() == ""){
		$(".bride-error").html("请填写新娘造型套数");
		$("#bride-style-count").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#groom-style-count").val() == ""){
		$(".groom-error").html("请填写新郎造型套数");
		$("#groom-style-count").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#outdoor-space").val() == ""){
		$(".outdoor-space-error").html("请填写外景地");
		$("#outdoor-space").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#inner-space").val() == ""){
		$(".inner-space-error").html("请填写内景地");
		$("#inner-space").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#photographer-level").val() == ""){
		$(".photographer-level-error").html("请填写摄影师级别");
		$("#photographer-level").focus().css("border","1px solid #f00");
		return false;
	}
	if($("#recommend-photographer").val() == ""){
		$(".recommend-photographer-error").html("请填写推荐摄影师");
		$("#recommend-photographer").focus().css("border","1px solid #f00");
		return false;
	}
	if($("#arter-level").val() == ""){
		$(".arter-level-error").html("请填写化妆师级别");
		$("#arter-level").focus().css("border","1px solid #f00");
		return false;
	}
	if($("#recommend-arter").val() == ""){
		$(".recommend-arter-error").html("请填写推荐化妆师");
		$("#recommend-arter").focus().css("border","1px solid #f00");
		return false;
	}
	
	$("input[type='checkbox']").each(function(){
		if($(this).attr("checked")) {
    			$(this).prop("checked",true);
   		}else{
   			$(this).prop("checked",false);
   		}
	})
	
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