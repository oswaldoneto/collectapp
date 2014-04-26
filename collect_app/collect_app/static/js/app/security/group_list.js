$(document).ready(function() {
	/* Settings */		
	$uic_open_button.button("option","disabled",true);
	$uic_delete_button.button("option","disabled",true);					
	$("#uic_group_table").dataTable({
		"bJQueryUI": true,		
		"bPaginate": false,
		"sPaginationType": "full_numbers",
		"bFilter":false,
		"bSort":true,
		"bInfo":false,
		"bAutoWidth":false,
		"aoColumns": [{ "bSortable": false },null],
		"aaSorting": [[ 1, "asc" ]],		
		"oLanguage": default_oLanguage								
	});
	/* Events */
	$("input:radio").click(function() {					 
		$( "#uic_open_button" ).button({ disabled: false });
		$( "#uic_delete_button" ).button({ disabled: false });
	});			
	$uic_open_button.click(function() {					 
		 var group_id = $("input:radio[name=group_selected]:checked").val();
		 redirect(sprintf('/security/group/%s/edit',group_id));
	});
	$uic_delete_button.click(function() {					 				
		$("#uic_delete_dialog").dialog({ 
			title:"Excluir Grupo",
			buttons: [
			{
				text: "Yes",
				click: function() { 
					var group_id = $("input:radio[name=group_selected]:checked").val();
					$("#uic_form").attr("action", sprintf('/security/group/%s/delete', group_id));  
					$("#uic_form").submit(); 
				}
			},
			{
				text: "No",
				click: function() { 
					$(this).dialog("close"); 
				}
			}					
		] });
	});			
});	
