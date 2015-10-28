/**
 * Created by jane on 15/6/11.
 */
$.fn.dropdown = function(settings){
    var defaults = {
        dropdownEl: '.dropdown-menu',
        openedClass: 'dropdown-open',
        delayTime: 100
    }
    var opts = $.extend(defaults, settings);
    return this.each(function(){
        var curObj = null;
        var preObj = null;
        var openedTimer = null;
        var closedTimer = null;
        $(this).hover(function(){
            if(openedTimer)
            clearTimeout(openedTimer);
            curObj = $(this);
            openedTimer = setTimeout(function(){
                curObj.addClass(opts.openedClass).find(opts.dropdownEl).show();
            },opts.delayTime);
            preObj = curObj;
        },function(){
            if(openedTimer)
            clearTimeout(openedTimer);
            openedTimer = setTimeout(function(){
                preObj.removeClass(opts.openedClass).find(opts.dropdownEl).hide();
            },opts.delayTime);
        });
        //点击事件关闭菜单
        $(this).bind('click', function(){
            if(openedTimer)
            clearTimeout(openedTimer);
            openedTimer = setTimeout(function(){
                preObj.removeClass(opts.openedClass).find(opts.dropdownEl).hide();
            },opts.delayTime);
        });
    });
};