$(document).ready(function() {
		
	$("#uic_new_button").click(function(){
		redirect(sprintf("/security/%s/add",security_url));
	});

	$("a[rel=uic_open_link]").click(function(){				
		redirect(sprintf('/security/group/%s/edit',$(this).attr('href')));
		return false;
	});

	$("a[rel=uic_delete_link]").click(function(){				
		$uic_delete_dialog = $('#uic_delete_dialog');
		$uic_delete_dialog.data("group_id",$(this).attr('href'));
		$uic_delete_dialog.modal('show');
		return false;
	});
	
	$("#uic_cancel_delete_group_button").click(function(){
		$('#uic_delete_dialog').modal('hide');				
	});
	
	$("#uic_confirm_delete_group_button").click(function(){
		$("#uic_form").attr("action", sprintf('/security/group/%s/delete', $('#uic_delete_dialog').data("group_id")));  
		$("#uic_form").submit(); 
	});

});	
