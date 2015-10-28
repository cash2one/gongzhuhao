/**
 * Created by hujunhao on 14/12/13.
 */

$(document).ready(function(){

    var uploader = $("#J-bg-FormFile");
    var uploader1 = $("#J-bg-FormFile1");
    var uploader2 = $("#J-bg-FormFile2");

    uploader.fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles : 1,
        maxFileSize: 500000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('.bg-img img').attr('src', file.url);
            });
        }
    });
    uploader.find("input:file").removeAttr('disabled');

    uploader1.fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles : 1,
        maxFileSize: 500000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('.bg-img1 img').attr('src', file.url);
            });
        }
    });
    uploader1.find("input:file").removeAttr('disabled');

    uploader2.fileupload({
        dataType: 'json',
        autoUpload: true,
        acceptFileTypes:  /(\.|\/)(gif|jpe?g|png)$/i,
        maxNumberOfFiles : 1,
        maxFileSize: 500000,
        done: function (e, data) {
            $.each(data.result.files, function (index, file) {
                $('.bg-img2 img').attr('src', file.url);
            });
        }
    });
    uploader2.find("input:file").removeAttr('disabled');

    $('.basic-info-save-btn').click(function(){
        var banner_url = $('.bg-img img').attr("src");
        var banner_url1 = $('.bg-img1 img').attr("src");
        var banner_url2 = $('.bg-img2 img').attr("src");
        var _xsrf = $('input[name="_xsrf"]').val();

        var result = true;     //全局保存判断

        if(result){
            if(banner_url==""){
                result = false;
                alert("请上传banner图片一！");
            }
        }
        if(result){
            if(banner_url1==""){
                result = false;
                alert("请上传banner图片二！");
            }
        }
        if(result){
            if(banner_url2==""){
                result = false;
                alert("请上传banner图片三！");
            }
        }
        if(result){
            var data_list = new Object();
            data_list.banner_url = banner_url;
            data_list.banner_url1 = banner_url1;
            data_list.banner_url2 = banner_url2;
            data_list._xsrf = _xsrf;

            jQuery.ajax({
                type: "POST",
                url: "/weixin/merchants/info/index",
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        alert('提交成功！');
                        location.href = "/weixin/merchants/info/index";
                    } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        }
    });

});