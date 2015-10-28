/**
 * Created by mele on 15/3/2.
 */
/*相册插件
 2015-02-26
 * */
var slider = function(options){
    this.options = options;
    this.sliderTop = 0;
    this.index = 0;
    this.loading = $(".photo-main .loading");
    this.photo = $(".photo-main .photo");
    this.wrap = $(".slider-photo-wrap");
}
slider.prototype = {
    init: function(){
        var that = this;
        $(this.options.wrap).each(function(index){
            $(this).attr("data-id",index);
        });
        that.bindEvents();
    },
    bindEvents: function(){
        var that = this;
        $("#slider-close").click(function(){
            that.close();
        });
        $("body").on("click",".masonry-brick a",function(e){
            e.preventDefault();
            that.index = $(this).closest(that.options.wrap).data("id");
            that.animate(that.index);
        });
        $("#photo-prev").click(function(){
            that.index != 0 ? that.index -- : that.index = $(that.options.wrap).length - 1;
            that.animate(that.index);
        });
        $("#photo-next").click(function(){
            that.index != $(that.options.wrap).length - 1 ? that.index ++ : that.index = 0;
            that.animate(that.index);
        });
    },
    animate: function(index){
        var that = this;
        var wrap = $(that.options.wrap);
        var a = wrap.eq(index).find(".example-image-link"),
            bigImg =  a[0].href != window.location.href ? a[0].href : a.find("img")[0].src,
            //desc = a.data("title"),
            num = $("#order-no").html(),
            type = $("#order-type").html(),
            name = $("#order-name").html(),
            mobile = $("#order-mobile").html(),
            id = a.data("id");
        if(!$("html").hasClass("o-hidden")){
            this.show();
        }
        if(this.photo[0].src != bigImg){
            this.load(bigImg);
        }
        this.loadDesc(index,num,type,name,mobile);
    },
    load: function(src){
        var that = this;
        this.photo.hide();
        this.loading.show();
        this.photo[0].src = src;
        this.photo.load(function(){
            that.loading.hide();
            $(this).show().height("auto");
            //获取图片高度
            var h = $(this).height();
            //动态设置高度
            that.resize(h);
            $(window).resize(function(){
                that.resize(h);
            })
        });
    },
    loadDesc: function(index,num,type,name,mobile){
        $(".slider-desc-review .info .length").html("当前页/总数："+(index-0+1)+"/"+$(this.options.wrap).length+"");//length
        $(".slider-desc-review .info .info-name").html("客户姓名：" + name);//desc
        $(".slider-desc-review .info .info-no").html("订单号：" + num);
        $(".slider-desc-review .info .info-type").html("订单类型：" + type);
        $(".slider-desc-review .info .info-mobile").html("联系方式：" + mobile);
        //$(".slider-desc-review .info h3").html(this.options.title?this.options.title:$(".slider-desc-review .info h3").html());
        //$(".slider-desc-review .info .face")[0].src = this.options.face;
        //$(".slider-desc-review .info .user-pic").attr("href",this.options.href);
        //$(".slider-desc-review .info .m-comment-li-desc a").text(this.options.name);
    },
    resize: function(h){
        if(h >= this.wrap.height()){
            this.photo.css("height",this.wrap.height()-20);
        }else{
            this.photo.css("height","auto");
        }
    },
    close: function(){
        $("#slider-pop-box").hide();
        $("#slider-mask").hide();
        $("html").removeClass("o-hidden");
        $("body").removeClass("o-hidden");
        $(document).scrollTop(this.sliderTop);
    },
    show: function(){
        $("#slider-pop-box").show();
        $("#slider-mask").show();
        this.sliderTop = $(document).scrollTop();
        $("html").addClass("o-hidden");
        $("body").addClass("o-hidden");
    }
}