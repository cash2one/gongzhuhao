$(document).ready(function(){
	var defaultTheme='cerulean';
	//var currentTheme=$.cookie('currentTheme')==null?defaultTheme:$.cookie('currentTheme');
	var msie=navigator.userAgent.match(/msie/i);
	$.browser={};
	$.browser.msie={};
	//switchTheme(currentTheme);
	$('.navbar-toggle').click(function(e){
		e.preventDefault();
		$('.nav-sm').html($('.navbar-collapse').html());
		$('.sidebar-nav').toggleClass('active');
		$(this).toggleClass('active');
	});
	var $sidebarNav=$('.sidebar-nav');
	$(document).mouseup(function(e){if(!$sidebarNav.is(e.target)
            && $sidebarNav.has(e.target).length === 0
            && !$('.navbar-toggle').is(e.target)
            && $('.navbar-toggle').has(e.target).length === 0
            && $sidebarNav.hasClass('active')
            )// ... nor a descendant of the container
        {
            e.stopPropagation();
            $('.navbar-toggle').click();
        }
    });

    //disbaling some functions for Internet Explorer
    if (msie) {
        $('#for-is-ajax').hide();
        $('#toggle-fullscreen').hide();
        $('.login-box').find('.input-large').removeClass('span10');

    }


    //highlight current / active link
    $('ul.main-menu li a').each(function () {
        if ($($(this))[0].href == String(window.location))
            $(this).parent().addClass('active');
    });

    // //establish history variables
    // var
    //     History = window.History, // Note: We are using a capital H instead of a lower h
    //     State = History.getState(),
    //     $log = $('#log');

    // //bind to State Change
    // History.Adapter.bind(window, 'statechange', function () { // Note: We are using statechange instead of popstate
    //     var State = History.getState(); // Note: We are using History.getState() instead of event.state
    //     $.ajax({
    //         url: State.url,
    //         success: function (msg) {
    //             $('#content').html($(msg).find('#content').html());
    //             $('#loading').remove();
    //             $('#content').fadeIn();
    //             var newTitle = $(msg).filter('title').text();
    //             $('title').text(newTitle);
    //             docReady();
    //         }
    //     });
    // });

    //ajaxify menus
    $('a.ajax-link').click(function (e) {
        if (msie) e.which = 1;
        if (e.which != 1 || !$('#is-ajax').prop('checked') || $(this).parent().hasClass('active')) return;
        e.preventDefault();
        $('.sidebar-nav').removeClass('active');
        $('.navbar-toggle').removeClass('active');
        $('#loading').remove();
        $('#content').fadeOut().parent().append('<div id="loading" class="center">Loading...<div class="center"></div></div>');
        var $clink = $(this);
        History.pushState(null, null, $clink.attr('href'));
        $('ul.main-menu li.active').removeClass('active');
        
        $clink.parent('li').addClass('active');
    });

    $('.accordion > a').click(function (e) {
        e.preventDefault();
        var $ul = $(this).siblings('ul');
        var $li = $(this).parent();
        if ($ul.is(':visible')) $li.removeClass('active');
        else                    $li.addClass('active');
        $ul.slideToggle();
    });

    $('.accordion li.active:first').parents('ul').show();
	//$('.accordion .nav-pills:first').slideDown();

    //other things to do on document ready, separated for ajax calls
    docReady();
});


function docReady() {
    //prevent # links from moving to top
    $('a[href="#"][data-top!=true]').click(function (e) {
        e.preventDefault();
    });


    $('.btn-close').click(function (e) {
        e.preventDefault();
        $(this).parent().parent().parent().fadeOut();
    });
    $('.btn-minimize').click(function (e) {
        e.preventDefault();
        var $target = $(this).parent().parent().next('.box-content');
        if ($target.is(':visible')) $('i', $(this)).removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        else                       $('i', $(this)).removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        $target.slideToggle();
    });
    $('.btn-setting').click(function (e) {
        e.preventDefault();
        $('#myModal').modal('show');
    });


}



//#提示信息弹出框
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

function show_dialog_reload(title,info){
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

function show_dialog_location_href(title,info,url){
        BootstrapDialog.show({
            title: title,
            message: info,
            buttons: [{
                label: 'OK',
                action: function(dialogItself){
                    dialogItself.close()
                    window.location.href = url
                }
            }]
        });
}

//生产随机数
function getRandom(n){
	return Math.floor(Math.random()*n+1)
}