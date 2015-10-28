$(function(){
	$(".write").click(function(){
		$(this).hide();
		$(this).parent().find(".write-box").css("display","inline-block");
	});
	
	
	$(".form-control").keyup(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #4cc25c");	
	});

	$(".form-control").blur(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");	
	});
	
	//字数统计
    $("#description").keyup(function(){
        var _curLength = $("#description").val().length;
        if(_curLength > 300){
            var _num = $("#description").val().substr(0, 300);
            $("#description").val(_num);
        }else{
          /*$("#txt-count").text($("#profile-info").val().length + '/300')*/
         	$("#txt-count").text("最多输入300字，您已输入：" + $("#description").val().length);
        }
    });		
    
    //图片提示显示与隐藏
	$(".up-photo").on({
		mouseenter: function(){
			$(this).find("a").css("z-index","99");
		},
		mouseleave: function(){
			$(this).find('a').css("z-index","-1");
		}
	});		
	
	//文本输入框大显示与隐藏
	//$('.tags[data-value="user_writing"]').click(function(){
	//	$(this).next(".input-write").css("display","inline-block").siblings(".input-write").hide();
	//})
	
	$(".form-group .tags").click(function(){
		$(this).addClass("current").siblings().removeClass("current");
		var self_write = $(this).attr('data-value');
		if(self_write=='user_writing'||self_write=='z_indoor_user_writing'||self_write=='z_outdoor_user_writing'){
		    if(self_write=='z_indoor_user_writing')
		        {
		            $(this).parent().find(".input-write").eq(0).show();
		            $(this).parent().find(".input-write").eq(1).hide();
		        }
		    else if(self_write=='z_outdoor_user_writing')
		        {
		            $(this).parent().find(".input-write").eq(1).show();
		            $(this).parent().find(".input-write").eq(0).hide();
		        }
		    else
		        $(this).parent().find(".input-write").show();
		       //.css("display","inline-block").siblings(".input-write").show();
		}else{
		    $(this).parent().find(".input-write").hide();//.next(".input-write").css("display","inline-block").siblings(".input-write").hide();
		    //.siblings(".input-write").hide();
		}
	});
	
	//根据类型显示不同的内容
	$('input[value="wedding"]').click(function(){
		$(".work-style").css("display","block");
		$(".work-shooting").css("display","none");
		$("#scene-weeding").css("display","inline-block");
		$("#scene-traveling").css("display","none");
	});
	
	$('input[value="traveling"]').click(function(){
		$(this).prop("checked",'true');
		$(".work-style").css("display","none");
		$(".work-shooting").css("display","block");
		$("#scene-weeding").css("display","none");
		$("#scene-traveling").css("display","inline-block");
	});

	
	$("input[type='checkbox']").each(function(){
		if($(this).attr("checked")) {
    			$(this).prop("checked",'true');
   		}
	})

	$("input:checkbox").click(function(){ 
		var len = $("input:checkbox:checked").length; 
		if(len > 2){ 
			alert('最多只能选两项哦！'); 
			return false; 
		} 
	}) 

	
	// $("input[type='radio']").click(function(){
	// 	if($(this).prop("checked")) {
 			// $(this).removeProp("checked");
	// 	}else{
	// 		$(this).prop("checked",'true');   			
	// 	}
	// })


	$("#save").click(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");		
        if(!checkForm())
            return;

    		//遍历所有被选中的checkbox选项
    		var _modeItem="";  
    		$("input[class='check-mode']:checked").each(function(){    
     		_modeItem += $(this).val() + ","; 
    		})     
   		//alert(_str);

		var _product_type = $("input[name='product_type']:checked").val();//婚纱摄影
		var _name = $("#series-name").val();//名称
		var _style_code = $("#work-style .current").attr("data-value");//婚纱风格
		
		var _sceneW = $("#scene-weeding .current").attr("data-value");
		var _sceneT = $("#scene-traveling .current").attr("data-value");
		
		
		//根据类型选择场景的值
		var _item = $("input[type='radio']:checked").val();
		if(_item == 'wedding'){
			var _shot_scene_code = $("#scene-weeding .current").attr("data-value");
			$("#scene-traveling .current").removeClass("current");
		}
		
		if(_item == 'traveling'){
			var _shot_scene_code = $("#scene-traveling .current").attr("data-value");
			$("#scene-weeding .current").removeClass("current");
		}
		
		
		var _shot_space = $("#work-shooting .current").text(); //旅行拍摄地
		
		var _sale_price = $("#sale-price").val();//起拍价
		var _description = $("#description").val();//描述
		var _cover_id = $("#cover").attr("data-id"); //封面图ID
		var _cover_url = $("#cover").attr("src");//封面图URL
		

    		
    		var _works_info = new Object(); //上传作品的图片ID以及描述信息
    		var _index = 0;
    		$(".photo-item").each(function(){
    			var imgItem = new Object();
			imgItem["id"] = $(this).find("img").attr("data-id");
			imgItem["desc"] = "";
			_works_info[_index] = imgItem;
			_index++;
    		});
		var images = JSON.stringify(_works_info);
	
		var _xsrf = $('input[name="_xsrf"]').val();
		var _work_id = $("#work-id").val();  //作品ID

		
		$.ajax({
			type:'POST',
			url:'/merchant/work/add/'+ _work_id +'/',
			data: {
				_xsrf:_xsrf,
				work_id: _work_id,
				product_type:_product_type,
				name: _name,
				style_code:_style_code,
				style_name:$('input[name="style_name"]').val(),
				shot_scene_code: _shot_scene_code,

				shot_scene_name_indoor:$('input[name="shot_scene_name_indoor"]').val(),
				shot_scene_name_outdoor:$('input[name="shot_scene_name_outdoor"]').val(),
				mode_style_code: _modeItem,
				shot_code: $("#work-shooting .current").attr("data-value"),
				shot_space: $('input[name="shot_space_name"]').val(),
				scene_traveling_name:$('input[name="scene_traveling_name"]').val(),
				sale_price: _sale_price,
				description: _description,
				cover_url:_cover_url,
				images:images
				//works_id:_works_id
			},
			success:function(data){
			    var result = eval("(" + data + ")");
				if(result.stat == 'ok'){
					$("#save").attr('disable','disable');
					$("#save").addClass("notAllow");
					show_dialog_reload("作品发布","发布成功");
					window.location.href = "/merchant/work/list/" + result.product_type;
				}else{
					show_dialog_reload("作品发布","发布失败");
				}
			},
			error: function(){
				
			}
		});
	});

	//删除图片
	$(".photo-thumb").on('click','.delete-photo', function(){
		var _html = $(this).parent();
		if(confirm("确定要删除吗？")){
		     work_img_id = $(this).attr('data-id');
		     $.get('/merchant/work/delete/img/'+work_img_id,{},function(data){
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

});
    
//校验文本输入区域不能为空
function checkForm(event){
	var moneyReg = /^[0-9]*[1-9][0-9]*$/;   //金钱只能输入数字
	var charReg = /^[\w\u4e00-\u9fa5]+$/gi;  //匹配中文，数字，字母和下划线
	
	if($("#series-name").val() == ''){
		$(".name-error").html("请填写名称！");
		$("#series-name").focus().css("border","1px solid #f00");
		return false;
	}
	if(!$("#series-name").val().match(charReg)){
		$(".name-error").html("您输入的内容含有特殊字符！");
		$("#series-name").focus().css("border","1px solid #f00");
		return false;
	}
	
	if($("#sale-price").val() == ''){
		$(".sale-price-error").html("请填写起拍价格！");
		$("#sale-price").focus().css("border","1px solid #f00");
		return false;
	}
	if(!$("#sale-price").val().match(moneyReg)){
		$(".sale-price-error").html("只能输入数字");
		$("#series-price").focus().css("border","1px solid #f00");
		return false;
	}
	
	$("input[type='radio']").click(function(){
		if($(this).prop("checked")) {
    			$(this).removeProp("checked");
   		}else{
			$(this).prop("checked",'true');   			
   		}

	})		
    return true;
}

$(document).ready(function() {
	var htmlTemplate = $('#J-model-photo').html();
	
	//上传封面图
	 $("#coverupload").click(function(){
	 	var uploader = $("#js_cover");
	 	addCover(uploader);
	 })
	 
	function addCover(uploader, i) {
	    uploader.fileupload({
	        dataType: 'JSON',
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

	            //var _html = '<img class="cover" id="cover" src="/static/crm/js/plugins/uploadify/img/user-loading.gif" data-id="" alt="" title="封面图" />';
	            //var _html = $('#J-model-cover').html();
	            //$("#coverupload").before(_html)
	             $("#cover").attr("src", "/static/crm/js/plugins/uploadify/img/user-loading.gif");
	        }
	    });
	    uploader.find("input:file").removeAttr('disabled');
	}	 
	 
	//上传图片
	$('#fileupload').click(function () {
	    var uploader = $("#J-formFile");
	    addPhoto(uploader);
	});

	function addPhoto(uploader) {
	    uploader.fileupload({
	        dataType: 'json',
	        autoUpload: true,
	        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
	        maxNumberOfFiles : 8,
	        maxFileSize: 5000000,
	        done: function (e, data) {
	        	console.log(data.result.stat);
	        	console.log(data.result.files[0].url);
	            $.each(data.result.files, function (index, file) {
	            	data.target.find('img').attr("src" , file.url).attr('data-id' , file.id);
	            	delete data.target;
	            });
	        },
	        send: function (e, data) {
	        	var target = $(htmlTemplate);
	        	data.target = target;
				$("#J-append-photo").append(target);
	        }
	    });
	    uploader.find("input:file").removeAttr('disabled');
	}	

});

