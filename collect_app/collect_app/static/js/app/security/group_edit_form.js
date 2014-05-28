$(document).ready(function() {		
	
	$('.ui.accordion').accordion();
	
	$("#uic_save_button").click(function(){
		$("#uic_form").attr("action",sprintf("/security/group/%s/edit",object_id));		
		$("#uic_form").submit(); 						
	});
	
	$("#uic_cancel_button").click(function(){
		redirect("/security/group/list");				 								
	});			

	$("#uic_classify_bundle_check").click(function() {
		var url = null;
		if ($("#uic_classify_bundle_check").is(":checked")) {
			url = "/security/permission/add";
		}
		else {
			url = "/security/permission/delete";
		}
		$.post(url,{
			'group':object_id,
			'bundle':'classify_bundle'
		}, function(data){
			$("#uic_success_feedback").show("fast");
			setTimeout(function() {
		        $("#uic_success_feedback").hide("slow");
		    }, 5000);    				
		})
		.error(function(){
			$("#uic_error_feedback").show("fast");
		});							
	});
	
	$("#uic_accounts_bundle_check").click(function() {
		var url = null;
		if ($("#uic_accounts_bundle_check").is(":checked")) {
			url = "/security/permission/add";
		}
		else {
			url = "/security/permission/delete";
		}
		$.post(url,{
			'group':object_id,
			'bundle':'manageacc_bundle'
		}, function(data){
			$("#uic_success_feedback").show("fast");
			setTimeout(function() {
		        $("#uic_success_feedback").hide("slow");
		    }, 5000);    				
		})
		.error(function(){
			$("#uic_error_feedback").show("fast");
		});							
	});			
	
	$.post("/security/permissions",{
		'group':object_id
	}, function(data){
		$("#uic_classify_bundle_check").attr('checked', data.classify_bundle);
		$("#uic_accounts_bundle_check").attr('checked', data.manageacc_bundle);
	})
	.error(function(){
	});	
});	
