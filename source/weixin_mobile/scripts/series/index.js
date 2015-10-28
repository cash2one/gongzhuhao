!(function(){

  $(function(){
    var page_code = 2 ,
        price = $("#price").val(),
      basepath = "/api/mobile/series/query/";

    //分页处理
    $(".btn-more").click(function(e){
      var url = basepath + page_code + "/" + price;
      var promise = $.get(url);
      promise.success(function(rs){
        rs = JSON.parse(rs);
        if(rs.has_next == 1){
          page_code += 1;
          $('.btn-more').show();
        }else{
          $(".btn-more").hide();
        }
        $('.content').append(rs.html);
      });

      promise.error(function(error){
        console.log(error);
      });
    });


    //图片晚加载
    // $(function() {
    //     $("img.lazy").lazyload();
    // });


  });

}());
