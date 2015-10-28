
function show_dialog_msg(title,info){
        BootstrapDialog.show({
            title: title,
            message: info,
            buttons: [{
                label: 'Close',
                action: function(dialogItself){
                    dialogItself.close()
                    window.location.reload()
                }
            }]
        });
}


function show_dialog_none_reload(title,info){
        BootstrapDialog.show({
            title: title,
            message: info,
            buttons: [{
                label: 'Close',
                action: function(dialogItself){
                    dialogItself.close()
                }
            }]
        });
}

var Conmmon = {
       change_passwd:function(user_id){
        alert('hello world');
        BootstrapDialog.show({
            message: $('<div></div>').load('/admin/users/new/')
        });

       }
};