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
		$("#uic_delete_dialog").dialog({
			title:"Deletar Documento",
			modal:true,
			buttons:[
				{
					text: "Yes",
					click: function() { 
						$("#uic_delete_form").attr("action", sprintf("/document/%s/delete",document_id));  
						$("#uic_delete_form").submit();
						return false;								
					}
				},
				{
					text: "No",
					click: function() { 
						$(this).dialog("close"); 
					}
				}					
			] 
		});
		return false;
	});		
	
	
	
	
});