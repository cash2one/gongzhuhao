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

	//自己写
	$(".form-group .tags").click(function(){
		$(this).addClass("current").siblings().removeClass("current");
		var self_write = $(this).attr('data-value');
		if(self_write=='user_writing'){
			$(this).parent().find(".input-write").eq(0).show();
		    $(this).parent().find(".input-write").eq(1).hide();
		}else{
		    $(this).parent().find(".input-write").hide();//.next(".input-write").css("display","inline-block").siblings(".input-write").hide();
		    //.siblings(".input-write").hide();
		}
	});

	//保存
	$("#save").click(function(){
		$(this).closest(".series").find(".error").html("");
	    $(this).css("border","1px solid #d8d8d8");		
	    if (!checkForm())
	        return;

		var _name = $("#work-name").val()
		var _category = $("#work-category .current").attr("data-value")
		var _color = $("#work-color .current").attr("data-value")
		var _style = $("#work-style .current").attr("data-value")

		if(_category == 'user_writing'){
			_category = $("input[name=category]").val()
		}
		if(_color == 'user_writing'){
			_color = $("input[name=color]").val()
		}
		if(_style == 'user_writing'){
			_style = $("input[name=style]").val()
		}

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
		var _post_url = $('input[name="post_url"]').val();

		$.ajax({
			type:'POST',
			url: _post_url,
			data: {
				_xsrf:_xsrf,
				name: _name,
				category: _category,
				color: _color,
				style: _style,
				sale_price: _sale_price,
				description: _description,
				cover_img:_cover_url,
				images:images
			},
			success:function(data){
			    var result = eval("(" + data + ")");
				if(result.stat == 'ok'){
					$("#save").attr('disable','disable');
					$("#save").addClass("notAllow");
					show_dialog_reload("作品发布","发布成功");
					window.location.href = "/merchant/weddingcompany/work/list/";
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
		     var work_img_id = $(this).parent().find("img").attr('data-id');
		     $.get("/merchant/weddingcompany/work/delete/img/"+work_img_id,{},function(data){
		     	if(data.stat == 'ok'){
		            _html.remove();
		        }else{
		           show_dialog_reload('删除失败');
		        }
		     }, 'JSON')
			return false;
		}
	});

});
    
//校验文本输入区域不能为空
function checkForm(event){
	var moneyReg = /^[0-9]*[1-9][0-9]*$/;   //金钱只能输入数字
	var charReg = /^[\w\u4e00-\u9fa5]+$/gi;  //匹配中文，数字，字母和下划线
	
	if($("#work-name").val() == ''){
		$(".work-error").html("请填写名称！");
		$("#work-name").focus().css("border","1px solid #f00");
		return false;
	}
	if(!$("#work-name").val().match(charReg)){
		$(".work-error").html("您输入的内容含有特殊字符！");
		$("#work-name").focus().css("border","1px solid #f00");
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