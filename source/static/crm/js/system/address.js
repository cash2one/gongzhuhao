$(function(){

	var _html = ['<li>',
                '<input type="hidden" value="" class="Fid" />',
				'<span class="addtxt" style="display:none"></span>',
				'<input type="text" class="form-control input-txt" style="display:inline-block" />',
				'<span class="glyphicon glyphicon-ok save" title="保存"></span>',
				'<span class="glyphicon glyphicon-edit edit" title="修改" style="display:none"></span>',
				'<span class="glyphicon glyphicon-trash delete" title="删除"></span>',
				'<span class="glyphicon glyphicon-cog set-default" title="设为默认"></span>',
				'</li>'
			].join('');

	$(".tip-address").on('click','.add',function(e){
		var _parentHtml = $(this).parent().find("ul");
		_parentHtml.append(_html);
		e.preventDefault();
		//console.log(_html);

        /*
		var _xsrf = $('input[name="_xsrf"]').val();
		$.ajax({
			type:"post",
			url:"",
			data:{
				_xsrf:_xsrf
			},
			success:function(data){
				if(data.stat == 'ok'){
					var _parentHtml = $(this).parent().find("ul");
					_parentHtml.append(_html);
					e.preventDefault();
					return false;
				}else{
					alert(data.msg);
				}
			},
			error: function(){
			}
		});
        */
	})

	//保存
	$(".ul-address").on('click','.save',function(){
		var _value = $(this).parent().find(".input-txt").val();
		var _fid = $(this).parent().find(".Fid").val();
		var _addtxt = $(this).parent().find(".addtxt");
        var _typeid = $(this).parent().parent().parent().find(".Ftype_id").val();
		var _this = $(".ul-address").find(".save");
		var _xsrf = $('input[name="_xsrf"]').val();

		$.ajax({
			type:"post",
			url:"/merchant/schedule/edit/template/site/",
			data:{
				_xsrf:_xsrf,
                Fsite: _value,
                Ftype_id: _typeid,
                Fid: _fid
			},
			success:function(data){
				_this.hide();
				_this.parent().find(".edit").show();
				$(".addtxt").show();
				_this.parent().find(".input-txt").hide();
				_addtxt.text(_value);
                window.location.reload();
			}
		});
	})


	//编辑
	$(".ul-address").on('click','.edit',function(){
		var _this = $(this).parent().find(".edit");
		var _text = $(this).parent().find(".addtxt").text();
        _this.parent().find(".addtxt").hide();
        _this.hide();
        _this.parent().find(".save").show();
        _this.parent().find(".input-txt").show();
        _this.parent().find(".input-txt").attr('value', _text);

	})

	//设置为默认值
	$(".ul-address").on('click','.set-default',function(){
		var _text = $(this).parent().find(".addtxt").text();
		var _this = $(this).find(".set-default");
		var _fid = $(this).parent().find(".Fid").val();
        var _typeid = $(this).parent().parent().parent().find(".Ftype_id").val();
		var _xsrf = $('input[name="_xsrf"]').val();

		$.ajax({
			type:"post",
			url:"/merchant/schedule/setdefault/template/site/",
			data:{
				_xsrf: _xsrf,
                Fid: _fid,
                Ftype_id: _typeid
			},
			success:function(data){
				_this.parent().find(".addtxt").hide();
				_this.hide();
				_this.parent().find(".save").show();
				_this.parent().find(".input-txt").show();
				_this.parent().find(".input-txt").attr('value', _text);
                window.location.reload();
			}
		});

	})

	//删除
	$(".ul-address").on('click','.delete',function(){
		var _fid = $(this).parent().find(".Fid").val();
		var _xsrf = $('input[name="_xsrf"]').val();
		var _html = $(this).parent();
	    BootstrapDialog.show({
	        title: '服务设置',
	        message: '删除成功',
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
							url:"/merchant/schedule/delete/template/site/",
							data: {
								_xsrf:_xsrf,
			                    Fid: _fid
							},
							success: function(data){
								if(data.stat == "ok"){
									show_dialog_none_reload("用户管理","删除成功！");
					                _html.remove();
								}else{
									show_dialog_reload("分享设置",data.msg);
								}
							},
							error: function(){
							}
						});                  
	            }
	        }]
	    });		
	})
})

function checkForm(){
	if($("input[type='text']").val() == ''){
		alert("请填写地址！");
		$(this).focue();
		return false;
	}
}
