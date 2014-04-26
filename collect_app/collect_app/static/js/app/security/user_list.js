
$(document).ready(function() {
	/* Settings */	
	$uic_open_button.button("option","disabled",true);
	$uic_delete_button.button("option","disabled",true);
	$("#uic_user_table").dataTable({
		"bJQueryUI": true,		
		"bPaginate": false,
		"sPaginationType": "full_numbers",
		"bFilter":false,
		"bSort":true,
		"bInfo":false,
		"bAutoWidth":false,
		"aoColumns": [{ "bSortable": false },null,null,null,{ "bSortable": false }],
		"aaSorting": [[ 1, "asc" ]],	
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
			title: "Excluir Usu�rio",
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
				text: "N�o",
				click: function() { 
					$(this).dialog("close"); 
				}
			}					
		] });
	});			
});	