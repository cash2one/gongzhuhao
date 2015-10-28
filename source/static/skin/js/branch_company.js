/**
 * Created by yijiaren-sun on 15-1-12.
 */
$(document).ready(function(){

    $('.delete').click(function(){
            if(confirm('确定要删除吗')){
                var id = $(this).parent().parent().attr('data-id');
                var _xsrf = $('input[name="_xsrf"]').val();
                $.ajax({
                type: "POST",
                url: "/merchant/branch/delete",
                data: {'id':id, '_xsrf': _xsrf} ,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;
                    if (stat == "ok") {
                        location.reload()
                   } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
            }
        });

        $('#new_branch').click(function(){
        $('input[name="id"]').val('');
        $('input[name="company_name"]').val('');
        $('input[name="detail_address"]').val('');
        $('.modal').modal();
        });

        $('#cancer').click(function(){
        $('.modal').modal('hide');
        });

        $('#save').click(function(){
        var id = $('input[name="id"]').val().trim();
        var name = $('input[name="company_name"]').val().trim();
        var province = $('.province').val();
        var city = $('.city').val();
        var area = $('.county').val();
        var address = $('input[name="detail_address"]').val().trim();
        var _xsrf = $('input[name="_xsrf"]').val();
        if (name == ''){
            $('.company-name-err').text("分店名称不能为空！");
            return
        }
        if (address == ''){
            $('.detail-address-err').text("详细地址不能为空！");
            return
        }
         var data_list = new Object();

            data_list.id = id;
            data_list.name = name;
            data_list.province = province;
            data_list.city = city;
            data_list.area = area;
            data_list.detail_address = address;
            data_list._xsrf = _xsrf;

            $.ajax({
                type: "POST",
                url: "/merchant/branch/edit",
                data: data_list,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;

                    if (stat == "ok") {
                        location.reload()
                   } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });
        });

        $('.edit').click(function(){
                var id = $(this).parent().parent().attr('data-id');
                $.ajax({
                type: "GET",
                url: "/merchant/branch/get",
                data: {'id':id} ,
                dataType: "JSON",
                success: function (data) {
                    var stat = data.stat;
                    if (stat == "ok") {
                       $('input[name="id"]').val(data.list['id'])
                       $('input[name="detail_address"]').val(data.list['detail_address']);
                       $('input[name="company_name"]').val(data.list['name']);
                       $('.province').val(data.list['province']);
                       loadSelect.addCity(data.list['city_list']);
                       $('.city').val(data.list['city']);
                       loadSelect.addCounty(data.list['area_list']);
                       $('.area').val(data.list['area']);
                       $('.modal').modal();
                   } else {
                        alert(data.msg);
                    }
                },
                error: function () {
                }
            });

        });


        $('input[name="company_name"]').change(function(){
        var name = $(this).val().trim();
        name!="" ? $('.company-name-err').text("") : $('.company-name-err').text("分店名称不能为空！");
        });
        $('input[name="detail_address"]').change(function(){
        var address = $(this).val().trim();
        address!="" ? $('.detail-address-err').text("") : $('.detail-address-err').text("详细地址不能为空！");
    });


     //省的切换，带动市和区县的变化
    $('.province').change(function(){
        var province_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/location/province/change/"+province_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;

                if (stat == "ok") {
                    loadSelect.addCity(data.city);
                    loadSelect.addCounty(data.area);
                }
            },
            error: function () {
            }
        });
    });

    //市的切换，带动区县的变化
    $('.city').change(function(){
        var city_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/location/area/"+city_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;
                stat == "ok" ? loadSelect.addCounty(data.list) : "";
            },
            error: function () {
            }
        });
    });

    var loadSelect = {
        addCity: function(city){    //加载市
            $('.city').empty();

            $.each(city, function(i){
                var option = '<option value="' + city[i].id + '">' + city[i].name + '</option>';
                $('.city').append(option);
            });
        },
        addCounty: function(area){    //加载县区
            $('.county').empty();

            $.each(area, function(i){
                var option = '<option value="' + area[i].id + '">' + area[i].name + '</option>';
                $('.county').append(option);
            });
        }
    };



});