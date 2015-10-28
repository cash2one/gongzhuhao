$(function(){
	$("#js_tag_photo .tags").click(function(){
		$(this).addClass("current").siblings().removeClass("current");
	})
	
	 var i = 0;
	 $("#fileupload").fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        // maxNumberOfFiles : 10,
        maxFileSize: 5000000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('#J-append-photo a:eq(' + i + ')').attr("data-id", file.id);
                $('#J-append-photo a:eq(' + i + ')').attr("href", file.url);
                $('#J-append-photo a:eq(' + i + ')').find("img").attr("src", file.url);
                if($('#clearfix a').length == 0){
                    $('.confirm_and_send').show();
                    location.href = '/merchant/album/photo/upload/'+$('#album_id').val()+'/adorn';
                }
                i++;
            });
        },
        send: function (e, data) {
            var html = $('#J-model-photo').html();
            $('#js-photo').after(html);
        },
        processstart : function(e , data){
        	i = 0;
        }
    });

    //上传照片
    function addPhoto(uploader, i) {
        uploader.fileupload({
            dataType: 'json',
            autoUpload: true,
            acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
            // maxNumberOfFiles : 10,
            maxFileSize: 5000000,
            done: function (e, data) {
                $.each(data.result.files, function (index, file) {
                    $('#J-append-photo a:eq(' + i + ')').attr("data-id", file.id);
                    $('#J-append-photo a:eq(' + i + ')').attr("href", file.url);
                    $('#J-append-photo a:eq(' + i + ')').find("img").attr("src", file.url);
                    if($('#clearfix a').length == 0){
                        $('.confirm_and_send').show();
                        // location.href = '/merchant/album/photo/upload/'+$('#album_id').val()+'/adorn';
                    }
                    i++;
                });
            },
            send: function (e, data) {
                var html = $('#J-model-photo').html();
                $('#js-photo').after(html);
            }
        });
        uploader.find("input:file").removeAttr('disabled');
    }

	$("#js_del_all").click(function(){
		if(confirm("确定要删除吗")){
			$(".photo-thumb").remove();
			return false;
		}
	})
	
	$("#js_tags").click(function(){
		$("#js_dialog_tag").show();
	})
	
	$(".close-tag").click(function(){
		$(this).parent().parent().parent().css("display","none");
		
	})
	
	$("#js_dialog_tag .tags").click(function(){
		$(this).addClass("current");
		$(this).find(".tags-del").show();
	})
	
	$(".tags-del").click(function(){
		$(this).css("display","none");
	})
	
	$(".check-tags").click(function(){
		$("#js_dialog_tag").show();
	})
	
	$(".btn-conform").click(function(){

		var _text1 = $("#style .current").text();
		var _html1 = '<span class="photoTags"><i class="glyphicon glyphicon-picture"></i>拍摄风格：' + _text1 + '</span>';
		
		var _text2 = $("#scene .current").text();
		var _html2 = '<span class="photoTags"><i class="glyphicon glyphicon-home"></i>拍摄场景：' + _text2 + '</span>';
		
		var _text3 = $("#clothes .current").text();
		var _html3 = '<span class="photoTags"><i class="glyphicon glyphicon-picture"></i>婚纱摄影：' + _text3 + '</span>';
		
		$(".tags-all").append(_html1 + _html2 + _html3);
		
		$(this).closest("#js_dialog_tag").find(".tags").find(".tags-del").hide();
		$(this).closest("#js_dialog_tag").find(".tags").removeClass("current");
	
		//$(".tips").text("添加标签成功！");

	
		$(this).closest("#js_dialog_tag").hide(); 		
	})
	
	$(".send").click(function(){
		if(confirm("照片发送后将不能再上传和删除照片，是否发送？")){
			//$("#fileupload").attr("disabled","disabled");
			$("#fileupload").css({
				"disabled":"disable",
				"cursor": "not-allowed"
			});
			
			$(".btn-uploadphoto").css({
				"cursor": "not-allowed",
				"background":"#ccc",
				"border":"1px solid #ccc"
			});
			return false;
		}
	})
	//添加标签
//	$(".add-tags").click(function(){
//		$("#js_dialog_tag").show();
//	})

//图片排序

$('#xu-save').click(function(){
			var sd=[];
			$('.pt-item').each(function(index, element) {
                sd[index]=($(this).attr('index'));
            });
			alert(sd);
			})
		
				
		function Pointer(x, y) {
			this.x = x ;
			this.y = y ;
		}
		function Position(left, top) {
			this.left = left ;
			this.top = top ;
		}
		$(".photo-thumb .pt-item").each(function(i) {
			this.init = function() { // 初始化
				this.box = $(this).parent() ;
				$(this).attr('pa',i);
				$(this).attr("index", i	).css({
					position : "absolute",
					left : this.box.offset().left,
					top : this.box.offset().top
				}).appendTo(".photo-thumb") ;
				this.drag() ;
			},
			this.move = function(callback) {  // 移动
				 $('.pt-item').each(function(i) {
				$('.photo-thumb ul li').eq(i).width($(this).find('img').width())
              });
				$(this).stop(true).animate({
					left : this.box.offset().left,
					top : this.box.offset().top
				}, 500, function() {
					if(callback) {
						callback	.call(this) ;
					}
				}) ;
			},
			this.collisionCheck = function() {
				var currentItem = this ;
				var direction = null ;
				$(this).siblings(".pt-item").each(function() {
					if(
						currentItem.pointer.x > this.box.offset().left &&
						currentItem.pointer.y > this.box.offset().top &&
						(currentItem.pointer.x < this.box.offset().left + this.box.width()) &&
						(currentItem.pointer.y < this.box.offset().top + this.box.height())
					) {
						// 返回对象和方向
						if(currentItem.box.offset().top < this.box.offset().top) {
							direction = "down" ;
						} else if(currentItem.box.offset().top > this.box.offset().top) {
							direction = "up" ;
						} else {
							direction = "normal" ;
						}
						this.swap(currentItem, direction) ;
					}
				}) ;
			},
			this.swap = function(currentItem, direction) { // 交换位置
				if(this.moveing) return false ;
				var directions = {
					normal : function() {
						var saveBox = this.box ;
						this.box = currentItem.box ;
						currentItem.box = saveBox ;
						this.move() ;
						$(this).attr("index", this.box.index()) ;
						$(currentItem).attr("index", currentItem.box.index()) ;
					},
					down : function() {
						// 移到上方
						var box = this.box ;
						var node = this ;
						var startIndex = currentItem.box.index() ;
						var endIndex = node.box.index(); ;
						for(var i = endIndex; i > startIndex ; i--) {
							var prevNode = $(".photo-thumb .pt-item[index="+ (i - 1) +"]")[0] ;
							node.box = prevNode.box ;
							$(node).attr("index", node.box.index()) ;
							node.move() ;
							node = prevNode ;
						}
						currentItem.box = box ;
						$(currentItem).attr("index", box.index()) ;
					},
					up : function() {
						// 移到上方
						var box = this.box ;
						var node = this ;
						var startIndex = node.box.index() ;
						var endIndex = currentItem.box.index(); ;
						for(var i = startIndex; i < endIndex; i++) {
							var nextNode = $(".photo-thumb .pt-item[index="+ (i + 1) +"]")[0] ;
							node.box = nextNode.box ;
							$(node).attr("index", node.box.index()) ;
							node.move() ;
							node = nextNode ;
						}
						currentItem.box = box ;
						$(currentItem).attr("index", box.index()) ;
						
					}
				}
				directions[direction].call(this) ;
			},
			this.drag = function() { // 拖拽
				var oldPosition = new Position() ;
				var oldPointer = new Pointer() ;
				var isDrag = false ;
				var currentItem = null ;
				$(this).mousedown(function(e) {
					e.preventDefault() ;
					oldPosition.left = $(this).position().left ;
					oldPosition.top =  $(this).position().top ;
					oldPointer.x = e.clientX ;
					oldPointer.y = e.clientY ;
					isDrag = true ;
					currentItem = this ;
					
				}) ;
				$(document).mousemove(function(e) {
					var currentPointer = new Pointer(e.clientX, e.clientY) ;
					if(!isDrag) return false ;
					$(currentItem).css({
						"opacity" : "0.8",
						"z-index" : 999
					}) ;
					var left = currentPointer.x - oldPointer.x + oldPosition.left ;
					var top = currentPointer.y - oldPointer.y + oldPosition.top ;
					$(currentItem).css({
						left : left,
						top : top
					}) ;
					currentItem.pointer = currentPointer ;
					// 开始交换位置
					

					currentItem.collisionCheck() ;
					
					
				}) ;
				$(document).mouseup(function() {
					if(!isDrag) return false ;
					isDrag = false ;
					currentItem.move(function() {
						$(this).css({
							"opacity" : "1",
							"z-index" : 0
						}) ;
						$('#xu-save').show()
					}) ;
				}) ;
			}
			this.init() ;
		}) ;


})
