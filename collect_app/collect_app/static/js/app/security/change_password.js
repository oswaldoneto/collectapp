$(document).ready(function() {
	$("#uic_save_button").click(function(){
		$("#uic_form").attr("action","/security/user/password/change");  
		$("#uic_form").submit(); 						
	});
	$("#uic_cancel_button").click(function(){
		redirect("/security/user/list");				 								
	});			
});	
