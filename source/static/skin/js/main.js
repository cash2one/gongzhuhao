/**
 * Created by hujunhao on 15/1/19.
 */
$(document).ready(function(){

    //首页计算器计算
    $('#start_deal').click(function(){
        $(this).attr("disabled", true);
        var form = $('#statrCalculateForm');
        var result = true;
        var rule1 = /^([1-9][0-9]{0,4}(\.[0-9]?[1-9])?)$|^(0\.[0-9]?[1-9])$/;
        var rule2 = /^\d$/;

        //房屋类型的选择判断
        var house_type = $('#house_type').val();
        if(house_type=="-1"){
            result = false;
            err("1");
        }

        //建筑面积的输入判断
        if(result){
            var home_area = $('#home_area').val();
            if(!rule1.test(home_area)){
                result = false;
                err("2");
            }
        }

        //阳台个数的输入判断
        if(result){
            var total_balcony = $('#total_balcony').val();
            if(!rule2.test(total_balcony) || total_balcony>10){
                result = false;
                err("3");
            }
        }

        //卫生间数的输入判断
        if(result){
            var total_toilet = $('#total_toilet').val();
            if(!rule2.test(total_toilet) || total_toilet==0 || total_toilet>10){
                result = false;
                err("4");
            }
        }

        //装修风格的选择判断
        if(result){
            var decorate_style = $('#decorate_style').val();
            if(decorate_style=="-1"){
                result = false;
                err("5");
            }
        }

        //提交计算器内容
        result ? form.submit() : "";
    });

    //计算器页面内容条件计算
    $('.star').click(function(){
        $(this).attr("disabled", true);
        var form = $('#statrCalForm');
        var result = true;
        var rule1 = /^([1-9][0-9]{0,4}(\.[0-9]?[1-9])?)$|^(0\.[0-9]?[1-9])$/;
        var rule2 = /^\d$/;

        //建筑面积的输入判断
        if(result){
            var home_area = $('#cal_area').val();
            if(!rule1.test(home_area)){
                result = false;
                err("2");
            }
        }

        //卫生间数的输入判断
        if(result){
            var total_toilet = $('#cal_toilet').val();
            if(!rule2.test(total_toilet) || total_toilet==0 || total_toilet>10){
                result = false;
                err("4");
            }
        }

        //阳台个数的输入判断
        if(result){
            var total_balcony = $('#cal_balcony').val();
            if(!rule2.test(total_balcony) || total_balcony>10){
                result = false;
                err("3");
            }
        }

        //提交计算器内容
        if(result){
            var house_type = $('#c_house_style .cal-info-active').attr("data-id");
            $('input[name="house_type"]').attr("value", house_type);

            var decorate_style = $('#c_design_style .cal-info-active').attr("data-id");
            $('input[name="decorate_style"]').attr("value", decorate_style);

            form.submit();
        }
    });

    //计算器条件未满足时，报出的错误
    function err(type){
        var msg = "";

        switch(type){
            case "1":
                msg = "请选择房屋类型！";
                break;
            case "2":
                msg = "请输入建筑面积,并保持格式正确！";
                break;
            case "3":
                msg = "请输入阳台个数,并保持格式正确！";
                break;
            case "4":
                msg = "请输入卫生间数,并保持格式正确！";
                break;
            case "5":
                msg = "请选择装修风格！";
                break;
        }

        $('#calErr').text(msg).slideDown();

        setTimeout(function(){
            $('#calErr').slideUp().empty();
            $('#start_deal').attr("disabled", false);
        },3000);
    }

    //首页分享精华装修日记和毕业照的切换
    $('.share-diary').click(function(){
        if(!$(this).hasClass("share-active")){
            $('.share-photo').removeClass("share-active");
            $(this).addClass("share-active");

            $('#J_share_photo_part').hide();
            $('#J_share_diary_part').show();
        }
    });
    $('.share-photo').click(function(){
        if(!$(this).hasClass("share-active")){
            $('.share-diary').removeClass("share-active");
            $(this).addClass("share-active");

            $('#J_share_diary_part').hide();
            $('#J_share_photo_part').show();
        }
    });

    //头部条件选择
    $('.select-things').click(function(){

        var _self = $(this);
        if(!_self.hasClass("cal-info-active")){
            $(this).closest(".cal-info-select").find(".select-things").removeClass("cal-info-active");
            _self.addClass("cal-info-active");
        }
    });

    //灵感小图切换
    $('.ins-s-part img').click(function(){
        var src = $(this).attr("data-src");
        $(this).closest("li").find(".ins-b-link img").attr("src", src);
    });
});