$(document).ready(function() {

	$('.ui.accordion').accordion();

	$('#id_username').attr('readonly', true);

	$('#id_last_login').attr('readonly', true);

	$('#id_date_joined').attr('readonly', true);

	$("#id_groups").multiselect({
		noneSelectedText: "Selecione os grupos",
		selectedList: 4
	});
						
	$("#uic_save_button").click(function(){
		var url = sprintf("/security/user/%s/edit",object_id);
		$("#uic_form").attr("action", url);  
		$("#uic_form").submit(); 						
	});
	
	$("#uic_cancel_button").click(function(){
		redirect("/security/user/list");				 								
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
			'user':object_id,
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
			'user':object_id,
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
		'user':object_id
	}, function(data){
		$("#uic_classify_bundle_check").attr('checked', data.classify_bundle);
		$("#uic_accounts_bundle_check").attr('checked', data.manageacc_bundle);
	})
	.error(function(){
	});		
	
});