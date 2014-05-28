$(document).ready(function(){
	
	invalid_username = $(document).data("invalid_username");
	invalid_password = $(document).data("invalid_password");
	invalid_credentials = $(document).data("invalid_credentials");

	if (invalid_username) {
		$('#id_username').transition('shake');		
		$('#id_username').focus();			
	}
	else if (invalid_password) {
		$('#id_password').transition('shake');				
		$('#id_password').focus();			
	}
	else if (invalid_credentials) {
		$('#id_username').transition('shake');				
		$('#id_password').transition('shake');				
		$('#id_password').focus();			
	}
	else {
		$('#id_username').focus();			
	}
	
	$("#uic_login").click(function(){	
		$("#uic_login_form").attr("action", "/login/");  
		$("#uic_login_form").submit(); 
	});
	
	$("input").keypress(function(event) {
	    if (event.which == 13) {
	        event.preventDefault();
	        $("form").submit();
	    }
	});	
	
	
	
});
