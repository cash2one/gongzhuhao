/**
 * Created by mele on 15/1/27.
 */
$("#J-answer").click(function(e){
    e.preventDefault();
    var _this = $(this),
        parent = _this.closest(".answer-other"),
        input = parent.find(".answer-input");
    if (input.hasClass('hide')) {
        input.removeClass('hide');
    }else{
        input.addClass('hide');
    }

})