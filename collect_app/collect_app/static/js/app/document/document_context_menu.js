$(document).ready(function() {
	var document_id = $(document).data("document_id");			
	$("#uic_dcm-preview_link").click(function(){
		redirect(sprintf("/document/%s/preview",document_id));		
		return false;
	});
	$("#uic_dcm-classify_link").click(function(){
		redirect(sprintf("/document/%s/classify",document_id));		
		return false;
	});
	$("#uic_dcm-permission_link").click(function(){
		redirect(sprintf("/document/%s/permission",document_id));		
		return false;
	});
	$("#uic_dcm-delete_link").click(function(){
		$uic_delete_dialog = $('#uic_delete_document_dialog');
		$uic_delete_dialog.modal('show');
		return false;
	});		
	
	$("#uic_cancel_delete_button").click(function(){
		$('#uic_delete_dialog').modal('hide');				
	});

	$("#uic_confirm_delete_button").click(function(){
		$("#uic_delete_document_form").attr("action", sprintf("/document/%s/delete",document_id));  
		$("#uic_delete_document_form").submit();
	});
	
	$("#uic_dcm-audit_link").click(function(){
		redirect(sprintf("/document/%s/audit",document_id));		
		return false;		
	});
	
});