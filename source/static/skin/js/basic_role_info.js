$(document).ready(function () {
    $('.role_member').change(function () {
        var roles = document.getElementById("roles"); //定位select
        var index_roles = roles.selectedIndex; // 选中索引
        var text_roles = roles.options[index_roles].text; // 选中文本
        var value_roles = roles.options[index_roles].value; // 选中值

        var roles_member = document.getElementById("roles_member"); //定位select
        var index_rm = roles_member.selectedIndex; // 选中索引
        var text_rm = roles_member.options[index_rm].text; // 选中文本
        var value_rm = roles_member.options[index_rm].value; // 选中值

        var mytype, TemO = document.getElementById("dynamic");
        var role_input = document.createElement("input");
        role_input.type = "text";
        var role_id = "role|";
        role_id = role_id + value_roles+"|"+createRandom(1000).toString();
        role_input.id = role_id;
        role_input.name = role_id;
        role_input.text = text_roles;
        role_input.value = text_roles;

        var rolemember_Input = document.createElement("input");
        rolemember_Input.type = "text";
        var id_name = "role_member|";
        id_name = id_name + value_rm+"|"+createRandom(1000).toString()
        rolemember_Input.name = id_name
        rolemember_Input.id = id_name;
        rolemember_Input.text = text_rm;
        rolemember_Input.value = text_rm;

        var input_delete = document.createElement("input");
        input_delete.type = "button";
        input_delete.id = "for_delete";
        input_delete.value = "删除1";
        input_delete.text = "删除1";
        TemO.appendChild(role_input);
        TemO.appendChild(rolemember_Input);
        TemO.appendChild(input_delete);
        var newline = document.createElement("br");//创建一个BR标签是为能够换行！
        TemO.appendChild(newline);
    });
    $('#form_project').on('click', '#for_delete', function () {
//       alert($("#for_delete").parent().attr('id'));
        var parent_id = $("#for_delete").parent().attr('id');
        var elem_child = document.getElementById(parent_id).childNodes;
        $("#" + parent_id).empty();
    });

    $('.roles').change(function () {
        var roles_id = $(this).val();
        jQuery.ajax({
            type: "GET",
            url: "/project_role/change/" + roles_id,
            data: {},
            dataType: "JSON",
            success: function (data) {
                var stat = data.stat;
                if (stat == "ok") {
                    $('.role_member').empty();
                    loadSelect.add_role_member(data.role_member, roles_id);
                }
                else {
                    $('.role_member').empty();
                }
            },
            error: function () {
            }
        });
    });

    var loadSelect = {
        add_role_member: function (user, roles_id) {    //加载member
            var optopn = '<option></option> ';

            $('.role_member').append(optopn);

            $.each(user, function (i) {
                var option = '<option value="' + user[i].name + '">' + user[i].nick + '</option>';
                $('.role_member').append(option);
            });
        }
    }

    function createRandom( n) {
        var ranNum = Math.ceil(Math.random()*n+1) ;
        return ranNum;
    }

});