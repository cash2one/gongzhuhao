$(function(){
	var params = {
		fileInput: $("#js_btn_upload").get(0),
		//dragDrop: $("#fileDragArea").get(0),
		upButton: $("#js_submit").get(0),
		url: $("#js_form").attr("action"),
		filter: function(files) {
			var arrFiles = [];
			for (var i = 0, file; file = files[i]; i++) {
				if (file.type.indexOf("image") == 0) {
					if (file.size >= 102400000) {
						alert('您这张"'+ file.name +'"图片大小过大，应小于100000k');	
					} else {
						arrFiles.push(file);	
					}			
				} else {
					alert('文件"' + file.name + '"不是图片。');	
				}
			}
			return arrFiles;
		},
		onSelect: function(files) {
			var html = '', i = 0;
			$("#js_preview").html('<div class="upload-loading"></div>');
			var funAppendImage = function() {
				file = files[i];
				if (file) {
					var reader = new FileReader()
					reader.onload = function(e) {
//						html = html + '<div id="uploadList-'+ i +'" class="upload-append-list"><p><strong>' + file.name + '</strong>'+ 
//							'<a href="javascript:" class="upload-delete" title="删除" data-index="'+ i +'">删除</a><br />' +
//							'<img id="uploadImage-' + i + '" src="' + e.target.result + '" class="upload-image" /></p>'+ 
//							'<span id="uploadProgress-' + i + '" class="upload-progress"></span>' +
//						'</div>';
						html = html + '<div id="uploadList-'+ i +'" class="upload-append-list">'+ 
							'<a href="javascript:" class="upload-delete" title="删除" data-index="'+ i +'"></a>' +
							'<img id="uploadImage-' + i + '" src="' + e.target.result + '" class="upload-image" />'+ 
							'<p><span id="uploadProgress-' + i + '" class="upload-progress"></span></p>' +
						'</div>';
						
						i++;
						funAppendImage();
					}
					reader.readAsDataURL(file);
				} else {
					$("#js_preview").html(html);
					if (html) {
						//删除方法
						$(".upload-delete").click(function() {
							h5File.funDeleteFile(files[parseInt($(this).attr("data-index"))]);
							return false;	
						});
						//提交按钮显示
						$("#js_submit").show();	
					} else {
						//提交按钮隐藏
						$("#js_submit").hide();	
					}
				}
			};
			funAppendImage();		
		},
		onDelete: function(file) {
			//$("#uploadList-" + file.index).fadeOut();
			$("#uploadList-" + file.index).remove();
		},
		onProgress: function(file, loaded, total) {
			var eleProgress = $("#uploadProgress-" + file.index), percent = (loaded / total * 100).toFixed(2) + '%';
			eleProgress.show().html(percent);
		},
		onSuccess: function(file, response) {
            //$("#js_info").append("<p>上传成功，图片地址是：" + response + "</p>");
            $("#js_info").append("<p>上传成功</p>");
            window.history.back(-1);
		},
		onFailure: function(file) {
			$("#js_info").append("<p>图片" + file.name + "上传失败！</p>");	
			$("#uploadImage-" + file.index).css("opacity", 0.2);
		},
		onComplete: function() {
			//提交按钮隐藏
			$("#js_submit").hide();
			//file控件value置空
			$("#js_btn_upload").val("");
			$("#js_info").append("<p>当前图片全部上传完毕，可继续添加上传。</p>");
		}
	};
	h5File = $.extend(h5File, params);
	h5File.init();	
})
