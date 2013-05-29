$(document).ready(function() {
	/* OnLoad ----- */
	var document_id = $(document).data("document_id");	
	fnRefreshPublicContainer(document_id);
	fnRefreshUserContainer(document_id);
	fnRefreshGroupContainer(document_id);
	
	$uic_back_button = $("#uic_back_button").button({
		text: true,
		icons: {
			primary: "ui-icon-carat-1-w"
		}
	});
	$uic_users_autocomplete =  $("#uic_users_autocomplete").autocomplete({
		source: get_users()
	});
	$uic_groups_autocomplete =  $("#uic_groups_autocomplete").autocomplete({
		source: get_groups()
	});	
	$uic_users_autocomplete.on( "autocompletefocus", function( event, ui ) {
		$uic_users_autocomplete.val(ui.item.label);
		return false;
	});
	$uic_groups_autocomplete.on( "autocompletefocus", function( event, ui ) {
		$uic_groups_autocomplete.val(ui.item.label);
		return false;
	});
	$uic_users_autocomplete.on( "autocompleteselect", function( event, ui ) {
		var user_id = ui.item.value;
		fnAddUserPermission(user_id,document_id,"read_document");		
		return false;
	});		
	$uic_groups_autocomplete.on( "autocompleteselect", function( event, ui ) {
		var group_id = ui.item.value;
		fnAddGroupPermission(group_id,document_id,"read_document");		
		return false;
	});		
	$("a[rel=uic_user_add_change_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnAddUserPermission(user_id,document_id,"change_document");
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_user_remove_change_permission_link');
		return false;
	});
	$("a[rel=uic_user_remove_change_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnRemoveUserPermission(user_id,document_id,"change_document");
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_user_add_change_permission_link');
		return false;	
	});
	$("a[rel=uic_user_add_delete_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnAddUserPermission(user_id,document_id,"delete_document");		
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_user_remove_delete_permission_link');
		return false;
	});
	$("a[rel=uic_user_remove_delete_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnRemoveUserPermission(user_id,document_id,"delete_document");		
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_user_add_delete_permission_link');
		return false;	
	});
	$("a[rel=uic_user_add_read_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnAddUserPermission(user_id,document_id,"read_document");		
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_user_remove_read_permission_link');
		return false;	
	});
	$("a[rel=uic_user_remove_read_permission_link]").live("click",function(){
		var user_id = $(this).attr('href');
		fnRemoveUserPermission(user_id,document_id,"read_document");		
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_user_add_read_permission_link');
		return false;	
	});
	$("a[rel=uic_group_add_change_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnAddGroupPermission(group_id,document_id,"change_document");
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_group_remove_change_permission_link');
		return false;
	});
	$("a[rel=uic_group_remove_change_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnRemoveGroupPermission(group_id,document_id,"change_document");
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_group_add_change_permission_link');
		return false;	
	});
	$("a[rel=uic_group_add_delete_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnAddGroupPermission(group_id,document_id,"delete_document");		
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_group_remove_delete_permission_link');
		return false;
	});
	$("a[rel=uic_group_remove_delete_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnRemoveGroupPermission(group_id,document_id,"delete_document");		
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_group_add_delete_permission_link');
		return false;	
	});
	$("a[rel=uic_group_add_read_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnAddGroupPermission(group_id,document_id,"read_document");		
		$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");
		$(this).attr('rel', 'uic_group_remove_read_permission_link');
		return false;	
	});
	$("a[rel=uic_group_remove_read_permission_link]").live("click",function(){
		var group_id = $(this).attr('href');
		fnRemoveGroupPermission(group_id,document_id,"read_document");		
		$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");
		$(this).attr('rel', 'uic_group_add_read_permission_link');
		return false;	
	});
	$uic_read_public_permission_link = $("#uic_read_public_permission_link").live("click",function(){
		if ($(this).children("i").hasClass("icon-check")) {
			fnRemovePublicPermission(document_id,"read_document");			
			$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");	
		}
		else {
			fnAddPublicPermission(document_id,"read_document");
			$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");			
		}
		return false;
	});
	
	$uic_change_public_permission_link = $("#uic_change_public_permission_link").live("click",function(){
		if ($(this).children("i").hasClass("icon-check")) {
			fnRemovePublicPermission(document_id,"change_document");			
			$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");	
		}
		else {
			fnAddPublicPermission(document_id,"change_document");
			$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");			
		}
		return false;
	});
	$uic_delete_public_permission_link = $("#uic_delete_public_permission_link").live("click",function(){
		if ($(this).children("i").hasClass("icon-check")) {
			fnRemovePublicPermission(document_id,"delete_document");			
			$(this).children("i").removeClass("icon-check").addClass("icon-check-empty");	
		}
		else {
			fnAddPublicPermission(document_id,"delete_document");
			$(this).children("i").removeClass("icon-check-empty").addClass("icon-check");			
		}	
		return false;
	});
});
function get_users() {
	var users = [];
	$.each(jQuery.parseJSON($(document).data("users")),function(){
		users.push({label:this.fields.username,value:this.pk});
	});
	return users;		
}
function get_groups() {
	var groups = [];
	$.each(jQuery.parseJSON($(document).data("groups")),function(){
		groups.push({label:this.fields.name,value:this.pk});
	});
	return groups;					
}
function fnHasPermission(perm, permlist) {
	if (jQuery.inArray(perm,permlist) > -1  ) { 
		return "True";
	} 
	else { 
		return "False"; 
	}		    	
}
function fnRefreshPublicContainer(document_id) {
	$.get(sprintf("/api/document/%s/permissions/public",document_id),{}, function(data){	
		if (fnHasPermission("read_document",data.permission) == "True") {
			$uic_read_public_permission_link.children("i").addClass("icon-check");
		} else {
			$uic_read_public_permission_link.children("i").addClass("icon-check-empty");
		}
		if (fnHasPermission("change_document",data.permission) == "True") {
			$uic_change_public_permission_link.children("i").addClass("icon-check");
		} else {
			$uic_change_public_permission_link.children("i").addClass("icon-check-empty");		
		}
		if (fnHasPermission("delete_document",data.permission) == "True") {
			$uic_delete_public_permission_link.children("i").addClass("icon-check");		
		} else {
			$uic_delete_public_permission_link.children("i").addClass("icon-check-empty");				
		}
	}).error(function(){
		alert('Erro');
	});	
}
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
			$("#uic_users_autocomplete").val('');
			$("#uic_users_autocomplete").autocomplete( "close" );
			$("#uic_user_template").tmpl(parameters).appendTo("#uic_users_container").live();
		});
	}).error(function(){
		alert('Erro');
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
		alert('Erro');
	});							
}
function fnAddUserPermission(user_id,document_id,permission) {
	$.post(sprintf("/api/document/%s/permission/%s/user/%s",document_id,permission,user_id),{}, function(data){
		if (data.length == 1) {
			fnRefreshUserContainer(document_id);
		}
	}).error(function(){
		alert('Erro');
	});							
}
function fnAddGroupPermission(group_id,document_id,permission) {
	$.post(sprintf("/api/document/%s/permission/%s/group/%s",document_id,permission,group_id),{}, function(data){
		if (data.length == 1) {
			fnRefreshGroupContainer(document_id);
		}
	}).error(function(){
		alert('Erro');
	});							
}
function fnRemoveUserPermission(user_id,document_id,permission) {
	$.ajax({
		url:sprintf("/api/document/%s/permission/%s/user/%s",document_id,permission,user_id),
		type:"DELETE",
		dataType:"json",
		success: function(data) {
			if (data.length == 0) {
				fnRefreshUserContainer(document_id);
			}
		}					
	});
}
function fnRemoveGroupPermission(group_id,document_id,permission) {
	$.ajax({
		url:sprintf("/api/document/%s/permission/%s/group/%s",document_id,permission,group_id),
		type:"DELETE",
		dataType:"json",
		success: function(data) {
			if (data.length == 0) {
				fnRefreshGroupContainer(document_id);
			}
		}					
	});
}
function fnAddPublicPermission(document_id,permission) {
	$.post(sprintf("/api/document/%s/permission/%s/public",document_id,permission),{}, function(data){
	}).error(function(){
		alert('Erro');
	});							
}
function fnRemovePublicPermission(document_id,permission) {
	$.ajax({
		url:sprintf("/api/document/%s/permission/%s/public",document_id,permission),
		type:"DELETE",
		dataType:"json",
		success: function(data) {
		}					
	});
}