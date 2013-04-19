$(document).ready(function() {
	/* Setting  */
	$uic_new_button = $("#uic_new_button").button({
		text: true,
		icons: {
			primary: "ui-icon-document"
		}
	});
	$uic_open_button = $("#uic_open_button").button({
		text: true,
		icons: {
			primary: "ui-icon-folder-open"
		},
	});				
	$uic_delete_button = $("#uic_delete_button").button({
		text: true,
		icons: {
			primary: "ui-icon-trash"
		},
	});
	/* Events */
	$uic_new_button.click(function() {
		redirect(sprintf("/security/%s/add",security_url));
	});
	$uic_open_button.click(function(){
		redirect(sprintf("/security/%s/list",security_url));
	});			
	if (object_id != null) {
		$uic_delete_button.click(function(){
			$("#uic_delete_dialog").dialog({ 
				title: "Excluir Usuário",
				buttons: [
				{
					text: "Yes",
					click: function() { 
						$("#uic_form").attr("action", sprintf('/security/%s/%s/delete',security_url,object_id));  
						$("#uic_form").submit(); 
					}
				},
				{
					text: "No",
					click: function() { 
						$(this).dialog("close"); 
					}
				}					
			]});
		});
	}
});