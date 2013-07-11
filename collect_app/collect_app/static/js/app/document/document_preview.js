$(document).ready(function() {
	/* OnLoad ----- */
	var document_id = $(document).data("document_id");	
	fnRefreshUserContainer(document_id);
	fnRefreshGroupContainer(document_id);
});
function fnRefreshUserContainer(document_id) {
	jQuery('#uic_users_container div').html(''); //clear div element
	$.get(sprintf("/api/document/%s/permissions/user",document_id),{}, function(data){
		$.each(data,function(){
			var parameters = [
				{ id : this.user_id,
				  name : this.username,
				  read : fnHasPermission("read_document",this.permission),
				  change : fnHasPermission("change_document",this.permission),
				  exclude : fnHasPermission("delete_document",this.permission), 
				},
			];
			$("#uic_user_template").tmpl(parameters).appendTo("#uic_users_container").live();
		});
	}).error(function(){
		redirectToErrorPage();
	});							
}
function fnRefreshGroupContainer(document_id) {
	jQuery('#uic_group_container div').html(''); //clear div element
	$.get(sprintf("/api/document/%s/permissions/group",document_id),{}, function(data){
		$.each(data,function(){
			var parameters = [
				{ id : this.group_id,
				  name : this.group_name,
				  read : fnHasPermission("read_document",this.permission),
				  change : fnHasPermission("change_document",this.permission),
				  exclude : fnHasPermission("delete_document",this.permission), 
				},
			];
			$("#uic_groups_autocomplete").val('');
			$("#uic_groups_autocomplete").autocomplete( "close" );
			$("#uic_group_template").tmpl(parameters).appendTo("#uic_group_container").live();
		});
	}).error(function(){
		redirectToErrorPage();
	});							
}
function fnHasPermission(perm, permlist) {
	if (jQuery.inArray(perm,permlist) > -1  ) { 
		return "True";
	} 
	else { 
		return "False"; 
	}		    	
}
