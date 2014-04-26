$(document).ready(function() {
	/*
	 * User Dialog
	 */
	$("#uic_user_table").dataTable({
        "bSort":false,
        "bInfo":false,
        "bPaginate": false,
        "sScrollY": "150px",
        "bFilter":true,
        "oLanguage": default_oLanguage
	});			
	$("a[rel='adduser_link']").click(function(){
		var user_id = $(this).attr('href');
		parent.fnSelectUserCallback(user_id);
		return false;
	});
	/*
	 * Group Dialog
	 */
	$("#uic_group_table").dataTable({
        "bSort":false,
        "bInfo":false,
        "bPaginate": false,
        "sScrollY": "150px",
        "bFilter":true,
        "oLanguage": default_oLanguage
	});			
	$("a[rel='addgroup_link']").click(function(){
		var group_id = $(this).attr('href');
		parent.fnSelectGroupCallback(group_id);
		return false;
	});	
});
