/**
 * Created by jane on 15/6/4.
 */
$(function(){
	//个人中心Tab功能
	//$("#js_tab li:first,#js_tabCon .tab-con:first").addClass("on");
	//	$("#js_tab li").each(function(i){
	//	$(this).click(function(){
	//		$(this).addClass("on").siblings().removeClass("on");
	//		$($("#js_tabCon .tab-con")[i]).show().siblings().hide();
	//	});
	//});

	//个人中心导航显示于隐藏
    //$(".gzh-header-nav").hover(function(){
     //   $(this).find(".gzh-nav").show();
     //   return false;
    //},function(){
     //   $(this).find(".gzh-nav").hide();
    //});


	//修改个人资料
	$(function(){
		$("#js_tabCon").on('click','#saveProfile', function(event){

			//checkForm();
			var nick = $("#nick").val();
			var realname = $("#realname").val();
			var sex = $(":radio:checked").val();
			var sign = $("#sign").val();

			$.ajax({
					type: "post",
					url:"/api/user/",
					data:{
						nick:nick,
						realname:realname,
						sex:sex,
						sign:sign
					},
					success: function(data){
						var obj = $.parseJSON(data);
						if(obj.stat == 1000){
							$(".profile-error").html("修改资料成功！");
							return false;
							event.prevent_default();
						} else {
							$(".profile-error").html(obj.info);
							return false;
						}
					},

					error: function(){
					}
			})
		})
	})

	//发送手机验证码
    var interVal;
    var count = 60;
    var curCount;
    var code = "";
    var codeLength = 4;

    $("#js_tabCon").on('click','#getCode', function(){
        curCount = count;
        var phone = $("#phone").val();
        if(phone != ""){
            for (var i = 0; i < codeLength; i++){
                code += parseInt(Math.random() * 9).toString();
            }
            $("#js_tabCon #getCode").attr("disabled","true");
            $("#js_tabCon #getCode").val(curCount + "秒后重发");

            interVal = window.setInterval(setRemainTime,1000);
            $.ajax({
                type: "get",
                dataType: "text",
                url:"/api/phone/code/" + phone + "/_code",
                data:{
                    phone: phone
                },
                success: function(data){
                    if(data.stat != "1000"){
                        $(".phone-error").html(data.info);
                        return false;
                    }
                },

                error: function(){

                }
            });
        }else{
            $(".phone-error").html("手机号码不能为空!");
            return false;
        }
    })

     function setRemainTime(){
        if(curCount == 0){
            window.clearInterval();
            $("#js_tabCon #getCode").removeAttr("disabled");
            $("#js_tabCon #getCode").val("重新获取验证码");
            code = "";
        }else{
            curCount --;
            $("#js_tabCon #getCode").val(curCount + "秒后重发");
        }
     }

	//绑定手机验证码
    $("#js_tabCon").on('click','#savePhone', function(){
		checkForm();
		var phone = $("#phone").val();
		var code = $("#code").val();

        $.ajax({
				type: "post",
				dataType: "text",
				url:"/api/user/",
				data:{
					phone:phone,
                    code:code
				},
				success: function(data){
                    var obj = $.parseJSON(data);
					if(obj.code == 200){
                        $(".phone-error").html("绑定手机号成功！");
					} else {
                        $(".phone-error").html(obj.info);
                        return false;
                    }
				},

				error: function(data){
                    var obj = $.parseJSON(data);
                    $(".phone-error").html(obj.info);
				}
        })
	})

	//修改密码
    $("#js_tabCon").on('click','#savePwd', function(){
		//checkForm();
		//var pre_passwd = $("#pre_passwd").val();
		var passwd = $("#passwd").val();
        var confirm_pwd = $("#confirm_pwd").val();
        $.ajax({
				type: "post",
				url:"/api/user/",
				data:{
					//pre_passwd:pre_passwd,
                    passwd:passwd,
                    confirm_pwd:confirm_pwd
				},
				success: function(data){
                    var obj = $.parseJSON(data);
					if(obj.code == 200){
                        $(".pwd-error").html("绑定手机号成功！");
                        return false;
                        data.prevent_default();
					} else {
                        $(".pwd-error").html(obj.info);
                        return false;
                    }
				},

				error: function(){
				}
        })
	})


    //上传头像
    $("#btn-upload").fileupload({
        url:'/api/user/',
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes: /(\.|\/)(gif|jpe?g|png)$/i,
        maxFileSize: 5000000,
        done: function (e, data) {
            var rsp_data = eval(data.result);
            $('#target, #target-thumbnail').attr('src',rsp_data['data']['head_url']);
            jcrop_api.destroy();
            initJcrop();
            $('.avatar-preview').show();
        },
        send: function (e, data) {
        },
        processstart : function(e , data){
        	i = 0;
        }
    });

    //裁减
    //function jcrop(){

        var jcrop_api,
            boundx,
            boundy,

            // Grab some information about the preview pane
            preview = $('#preview-pane'),
            pcnt = $('#preview-pane .preview-container'),
            pimg = $('#preview-pane .preview-container img'),

            xsize = pcnt.width(),
            ysize = pcnt.height(),
            coords = [0,0,0,0];

        initJcrop();

        function initJcrop(){
            $('#target').Jcrop({
                onChange: updatePreview,
                onSelect: updatePreview,
                aspectRatio: xsize / ysize,
                boxWidth:300,
            },function(){
                var bounds = this.getBounds();
                boundx = bounds[0];
                boundy = bounds[1];
                jcrop_api = this;
                var img = $('#target');
                jcrop_api.animateTo([(img.width()-100)/2,(img.height()-100)/2,(img.width()-100)/2+100,(img.height()-100)/2+100]);
                preview.appendTo(jcrop_api.ui.holder);
            });
        }

        function updatePreview(c){
            if (parseInt(c.w) > 0) {
                var rx = xsize / c.w;
                var ry = ysize / c.h;
                pimg.css({
                    width: Math.round(rx * boundx) + 'px',
                    height: Math.round(ry * boundy) + 'px',
                    marginLeft: '-' + Math.round(rx * c.x) + 'px',
                    marginTop: '-' + Math.round(ry * c.y) + 'px'
                });
            }
            //coords = [parseInt(c.x), parseInt(c.y), parseInt(c.x2), parseInt(c.y2), parseInt(c.w), parseInt(c.h)]
        };

        $("#btn-save-avatar").on('click', function(){
            var params = {
                url: $('#target').attr('src'),
                x: coords[0],
                y: coords[1],
                x1: coords[2],
                y1: coords[3],
                bounds: [coords[4], coords[5]],
                getBounds: jcrop_api.getWidgetSize(),
                jcrop: jcrop_api.tellScaled()
            }
            $.post('/api/user/',params,function (data) {
                    var obj = $.parseJSON(data);
                    if (obj.stat == '1000') {
                        $('#current-avatar').attr('src', obj.data.head_url_thumb);
                        $('.avatar-preview').hide();
                    } else {
                        $(".avatar-error").html(obj.info);
                    }
                })
        })
    //}

})