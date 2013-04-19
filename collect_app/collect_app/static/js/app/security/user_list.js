
$(document).ready(function() {
	/* Settings */	
	$uic_open_button.button("option","disabled",true);
	$uic_delete_button.button("option","disabled",true);
	$("#uic_user_table").dataTable({
		"bJQueryUI": true,		
		"bPaginate": true,
		"sPaginationType": "full_numbers",
		"bFilter":false,
		"bSort":true,
		"bInfo":true,
		"bAutoWidth":false,
		"aoColumns": [{ "bSortable": false },null,null,null,{ "bSortable": false }],
		"oLanguage": default_oLanguage				
	});
				
	/* Events */
	$("input:radio[name=user_selected]").click(function() {					 
		$uic_open_button.button("option","disabled",false);
		$uic_delete_button.button("option","disabled",false);
	});			
	$uic_open_button.click(function() {
		 var user_id = $("input:radio[name=user_selected]:checked").val();
		 redirect(sprintf('/security/user/%s/edit',user_id));
	});
	$uic_delete_button.click(function() {					 				
		$("#uic_delete_dialog").dialog({ 
			title: "Excluir Usuário",
			buttons: [
			{
				text: "Sim",
				click: function() { 
					var user_id = $("input:radio[name=user_selected]:checked").val();
					$("#uic_form").attr("action", sprintf('/security/user/%s/delete', user_id));  
					$("#uic_form").submit(); 
				}
			},
			{
				text: "Não",
				click: function() { 
					$(this).dialog("close"); 
				}
			}					
		] });
	});			
});	