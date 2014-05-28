$(document).ready(function() {
	/* Events */			
	$("#uic_save_button").click(function(){
		$("#uic_form").attr("action","/security/user/add");  
		$("#uic_form").submit(); 						
	});
	$("#uic_cancel_button").click(function(){
		redirect("/security/user/list");				 								
	});			
});	
