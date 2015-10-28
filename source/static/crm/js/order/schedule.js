$(function(){
	$('input[name^="shd_date_"],input[name^="shd_site_"],input[name^="shd_tips_"],input[name^="shd_stff_id_"],\
	input[name^="shd_stff_tt_"],input[name^="shd_stff_nm_"]').change(function(){
		$(this).closest('tr').find('input[name^="is_modify_"]').val(1);
	});

	var mydate = new Date();
    var str = mydate.getFullYear() + "-";
    str += (mydate.getMonth()+1) + "-";
    str += mydate.getDate() + ' ';
 
 	console.log(str);
	
	
	$('.datatime').datetimepicker({
		lang:'ch',
		format:'Y-m-d H:i',
		formatDate:'Y-m-d H:i',
		step:'30',
		allowTimes:[ '1:00','1:30','2:00','3:30', '3:00','4:00','4:30','5:00','5:30','6:00','6:30','7:00',
		'7:30','8:00','8:30','9:00', '8:30','10:00','10:30','11:00', '11:30','12:00','12:30','13:00','13:30',
		'14:00','14:30','15:00','15:30','16:00','16:30','17:00','17:30','18:00','18:30','19:00','19:30','20:00','20:30',
		'21:00','21:30','22:00','22:30','23:00','23:30','24:00','0:30'],
		onShow:function( ct ){
			this.setOptions({
		    		minDate:str?str:false
		   	})
		  },
		  scrollInput:false,
//		  defaultSelect:false,
		  validateOnBlur:false

	});

	
	$("#cancel").click(function(){
		window.location.href = "/merchant/orders/list/7"
	})

    $(".input_text").click(function(){
        text = $(this).html();
        $(this).parent().parent().parent().parent().find("input").val(text);
    })
})


