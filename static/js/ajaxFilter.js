var csrftoken = Cookies.get('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
	// crossDomain: false,
	timeout:20000,
	beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }

});

$(document).ready(function(){

	// Submit YNA filter set value to backend
	$("#submit-btn").click(function(){
		$("#feature_accordion .collapse").collapse('hide'); //close all collapse
		let jdata = {};
		for (var i = 1; i < 5; i++) {
			
			chk_box = $("#collapse" + String(i) +" .feature-checkbox:checked");
			// console.log(chk_box);
			jdata[i] = chk_box.map(function(){
				let select = $(this).closest('div.row').find('select');
				let type = select.eq(0).val();
				let compare = select.eq(1).val();
				let value = $(this).closest('div.row').find('input.value').val();
				return $(this).val() + "_" + type + "_" + compare + "_" + value;
			}).get();
		};
	
		$.ajax({
	    	url:"/result/",
	    	data:{
	    		jdata: JSON.stringify(jdata),
	    	},
	    	type:"POST",
	    	success:function(d){
	    		$("#resultDiv").html(d);
	    		$("#result_table").DataTable();
	    		// console.log(d);
	    	},
	    });


	});
		
});