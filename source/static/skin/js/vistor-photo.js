/*瀑布流开始*/

var start = new slider({
    wrap:".masonry-brick",
    title: $("#J-decoration-theme").text(),
    face: $("#J-user-head").attr("src"),
    href: $("#J-user-link").attr("href"),
    name: $("#J-user-name").text()
});

var water = (function(){
    var userId = parseInt(window.location.href.split("/").pop());
    var container = $('.uploaded-photos-list');
    var loading=$('#imloading');
    var columnCount = 3;
    var columnW = 301;
    var gutterWidth = (container.width()-(columnCount*columnW))/(columnCount-1);
//    gutterWidth = 100;
// 初始化loading状态
    loading.data("on",false);
    //初始化page
    $("#page").val("1");

//初始化插件
    container.imagesLoaded(function(){
        container.masonry({
            columnWidth: columnW,
            gutterWidth: gutterWidth,
            itemSelector : '.item',
            isFitWidth: false,//是否根据浏览器窗口大小自动适应默认false
            isAnimated: false,//是否采用jquery动画进行重拍版
            isRTL:false,//设置布局的排列方式，即：定位砖块时，是从左向右排列还是从右向左排列。默认值为false，即从左向右
            isResizable: true,//是否自动布局默认true
            animationOptions: {
                duration: 600,
                easing: 'easeInOutBack',//如果你引用了jQeasing这里就可以添加对应的动态动画效果，如果没引用删除这行，默认是匀速变化
                queue: true//是否队列，从一点填充瀑布流
            }
        });
    });
//initLoad
    function initLoad(func){
        $.ajax({
            url: "/member/decorate_album/get/"+userId,
            type: "post",
            dataType: "json",
            data: {
                _xsrf: $('input[name="_xsrf"]').val(),
                page: $("#page").val()
            },
            beforeSend: function(){
                loading.text("正在加载...");
            },
            success: function(response){
                if (response.stat == "ok") {
                    var html="";
                    var list = response.list;
                    if (list.length) {
                        for(var i in list){
                            html+='<li class="item">'+
                            '<div class="list-line photo-list-id" data-id="'+list[i].id+'">'+
                            '<div class="up-photo">'+
                            '<a class="example-image-link" href="'+list[i].orig_url+'" data-lightbox="example-set" data-title="'+list[i].desc+'"><img data-count="'+list[i].assist_count+'" id="'+list[i].id+'" class="example-image" src="'+list[i].url+'" alt="" title=""></a>'+
                            '</div>'+
                            '</div>'+
                            '</li>';
                        }
                    }else{
                        $("#Gallery").html("还没有上传毕业照。");
                        return;
                    }
                    setTimeout(function(){
                        /*延时800毫秒,防止动画期间重复加载*/
                        $(html).find('img').each(function(index){
                            loadImage($(this).attr('src'));
                        })
                        var $newElems = $(html).css("opacity",0).appendTo(container);
                        $newElems.imagesLoaded(function(){
                            $newElems.animate({"opacity":1},600);
                            container.masonry( 'appended', $newElems,true);
                            setTimeout(function(){
                                loading.text("加载更多");
                                if(!response.has_more){
                                    loading.hide();
                                }else{
                                    loading.data("on",true);
                                    $("#page").val(response.total_page);
                                }
                                //callBack
                                if(func)func();
                            },600);
                        });
                    },600);
                }
            }
        });
    };
//初始化
    initLoad(function(){
        start.init();
        //滚动事件
        $(window).scroll(function(){
            if(!loading.data("on")) return;
            var itemNum=container.find('.item').length;
            var itemArr=[];
            itemArr[0]=container.find('.item').eq(itemNum-1).offset().top+container.find('.item').eq(itemNum-1)[0].offsetHeight;
            itemArr[1]=container.find('.item').eq(itemNum-2).offset().top+container.find('.item').eq(itemNum-1)[0].offsetHeight;
            itemArr[2]=container.find('.item').eq(itemNum-3).offset().top+container.find('.item').eq(itemNum-1)[0].offsetHeight;
            var maxTop=Math.max.apply(null,itemArr);
            if(maxTop<$(window).height()+$(document).scrollTop()){
                loading.data("on",false).fadeIn(800);
                initLoad(function(){
                    $(start.options.wrap).each(function(index){
                        $(this).attr("data-id",index);
                    });
                });
            }
        });
    })
})();


//图片预加载
function loadImage(url) {
    var img = new Image();
    //创建一个Image对象，实现图片的预下载
    img.src = url;
    if (img.complete) {
        return img.src;
    }
    img.onload = function () {
        return img.src;
    };
};
