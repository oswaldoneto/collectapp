$(document).ready(function(){	
	$("#uic_newdoc_link").click(function(){
		redirect("/document/new/classify");
		return false;
	});
	$("#uic_search_link").click(function(){
		redirect("/search");
		return false;
	});
	$("#uic_category_link").click(function(){
		redirect("/category/list");
		return false;
	});
	$("#uic_tag_link").click(function(){
		redirect("/tag/list");
		return false;
	});
	$("#uic_user_link").click(function(){
		redirect("/security/user/list");
		return false;
	});
	$("#uic_group_link").click(function(){
		redirect("/security/group/list");
		return false;
	});
	
	$("#uic_changepassword_link").click(function(){
		redirect("/security/user/password/change");
		return false;
	});
	$("#uic_logout_link").click(function(){
		redirect("/logout");
		return false;
	});
	$("#uic_lookup_link").click(function(){
		$("#uic_form").submit(); 
		return false;			
	});
});