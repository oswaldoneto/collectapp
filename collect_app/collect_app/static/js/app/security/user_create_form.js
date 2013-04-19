$(document).ready(function() {
	/* Settings */						
	$uic_delete_button.button("option","disabled",true);
	/* Events */			
	$("#uic_save_button").button().click(function(){
		$("#uic_form").attr("action","/security/user/add");  
		$("#uic_form").submit(); 						
	});
	$("#uic_cancel_button").button().click(function(){
		redirect("/security/user/list");				 								
	});			
});	
