/**
 * Created by mele on 15/3/2.
 */
/*相册插件
 2015-02-26
 * */
var slider = function(options){
    this.options = options;
    this.index = 0;
    this.loading = $(".photo-main .loading");
    this.photo = $(".photo-main .photo");
    this.wrap = $(".slider-photo-wrap");

    this.module1 = $("#comment-module").html();
    this.module2 = $("#comment-module-reply").html();
    this.comment_textarea = $("#comment-textarea").html();
    this.like_list = {};
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
        //评论
        $(document).on("click",".review-submit",function(){
            if(Base.isLogin()) {
                that.addComment($("#review-submit").data("pic"),
                    $(this).data("parent_comment_id") == "0" ? $(this).data("id") : $(this).data("parent_comment_id"),
                    $(this).closest("div").find("textarea").val(),
                    $(this).data("target_user_id"),
                    $(this).data("target_user_id") == "0" ? that.module1 : that.module2,
                    $(this).data("target_user_id") == "0" ? $(".review-list") : $(this).closest("li"));
            }
        });
        //评论框
        $(document).on("click",".comment-this",function(){
            $(".huifu").remove();
            var textarea = that.replaceCommentModel(that.comment_textarea,$(this).data());
            $(this).closest(".m-comment-list-item").after(textarea);
        });
    },
    animate: function(index){
        var that = this;
        var wrap = $(that.options.wrap);
        var a = wrap.eq(index).find(".example-image-link"),
            bigImg =  a[0].href != window.location.href ? a[0].href : a.find("img")[0].src,
            desc = a.data("title"),
            id = a.find("img")[0].id,
            count = a.find("img").data("count");
        if(!$("html").hasClass("o-hidden")){
            this.show();
        }
        if(this.photo[0].src != bigImg){
            this.load(bigImg);
        }
        this.loadDesc(index,desc);
        this.loadCommentList(id);
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
    loadDesc: function(index,desc){
        $(".slider-desc-review .info .length").html("("+(index-0+1)+"/"+$(this.options.wrap).length+")");//length
        $(".slider-desc-review .info .desc").html(desc);//desc
        $(".slider-desc-review .info h3").html(this.options.title?this.options.title:$(".slider-desc-review .info h3").html());
        $(".slider-desc-review .info .face")[0].src = this.options.face;
        $(".slider-desc-review .info .user-pic").attr("href",this.options.href);
        $(".slider-desc-review .info .m-comment-li-desc a").text(this.options.name);
    },
    loadCommentList: function(id){
        var that = this;
        var comment = "";
        $("#review-submit").attr("data-pic",id);
        $(".review-list").empty();
        $.get("/comment/image/"+id,function(data){
            //like
            $(".slider-pop-box .like").attr("data-id",id).text(data.assist_count).show();
            if(data.is_like){
                $(".slider-pop-box .like").removeClass("un");
            }else{
                $(".slider-pop-box .like").addClass("un");
            }
            $.each(data.list,function(i,n){
                comment = that.replaceCommentModel(that.module1,this);
                if(this.reply_list.length){
                    var replay = that.replaceCommentModel(that.module2,this.reply_list);
                    comment+=replay;
                }
                $(".review-list").append(comment);
                $("li").nextAll(".m-comment-list-item").appendTo($("li").nextAll(".m-comment-list-item").prev("li"));

            })
        },"json");

    },
    addComment: function(id,parent_comment_id,text,target_user_id,module,wrap){
        var that = this;
        $.post("/comment/image/"+id,{p_id:parent_comment_id,text:text,user_id:target_user_id,_xsrf:$("#_xsrf").val()},function(data){
            if(data.stat == "ok"){
                if(module == that.module1){
                    wrap.prepend(that.replaceCommentModel(module,data.list));
                    $("#review-text").val("");
                }else{
                    wrap.append(that.replaceCommentModel(module,data.list));
                    $(".huifu").remove();
                }
            }
        },"json")
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
    },
    show: function(){
        $("#slider-pop-box").show();
        $("#slider-mask").show();
        $("html").addClass("o-hidden");
        $("body").addClass("o-hidden");
    },
    replaceCommentModel: function(html,list){
        if(list.length == undefined){
            $.each(list,function(i,k){
                    var reg = new RegExp("{"+i+"}","g");
                    html = html.replace(reg, k);
            })
        }else{
            var reply="";
            for(var i in list){
                var each=html;
                $.each(list[i],function(i,k){
                        var reg = new RegExp("{"+i+"}","g");
                        each = each.replace(reg, k);
                });
                reply+=each;
            }
            html = reply;
        }
        return html;
    }
}


//比较时间
function StringToDate(DateStr)
{
    var converted = Date.parse(DateStr);
    var myDate = new Date(converted);
    if (isNaN(myDate))
    {
        var arys= DateStr.split('-');
        myDate = new Date(arys[0],--arys[1],arys[2]);
    }
    return myDate;
}
Date.prototype.DateDiff = function(strInterval, dtEnd) {
    var dtStart = this;
    if (typeof dtEnd == 'string' )//如果是字符串转换为日期型
    {
        dtEnd = StringToDate(dtEnd);
    }
    switch (strInterval) {
        case 's' :return parseInt((dtEnd - dtStart) / 1000);
        case 'n' :return parseInt((dtEnd - dtStart) / 60000);
        case 'h' :return parseInt((dtEnd - dtStart) / 3600000);
        case 'd' :return parseInt((dtEnd - dtStart) / 86400000);
        case 'w' :return parseInt((dtEnd - dtStart) / (86400000 * 7));
        case 'm' :return (dtEnd.getMonth()+1)+((dtEnd.getFullYear()-dtStart.getFullYear())*12) - (dtStart.getMonth()+1);
        case 'y' :return dtEnd.getFullYear() - dtStart.getFullYear();
    }
}
