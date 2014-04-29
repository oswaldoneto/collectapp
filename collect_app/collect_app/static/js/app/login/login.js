$(document).ready(function(){

	$("#uic_login").click(function(){
		$("#uic_login_form").attr("action", "/login/");  
		$("#uic_login_form").submit(); 
	});

});
