
var $uic_tags = null;

$(document).ready(function() {
	/* OnLoad ----- */
	var document_id = $(document).data("document_id");	
	fnRefreshUserContainer(document_id);
	fnRefreshGroupContainer(document_id);
	
	$.get(sprintf("/api/document/%s/tag",document_id),{},function(data){

		//TODO: is it possible become hack behavior part of the tag-it?
		//hack to disable on tag added event until load current tags,
		//this don´t allow post request during loading
		$(document).data("disarm_on_tagadded",false);
		
		//tag-it component
		$uic_tags = $("#uic_tags").tagit({
			createTagOnBlur:false,
			
    		availableTags:fnListTagLabel(data.all_tags),
    			
			onBeforeTagAdded:function(event,tag) {
	        	if (fnGetTagId(tag.text(),data.all_tags) == null) {
        			$.fancybox.open([{
							href : sprintf('/tag/dialog?name=%s',tag.text())
					    }], {
							'type' 			: 'iframe',
							'autoScale' 	: false,
							'autoDimensions': false,
							'width' 		: 400,
							'height' 		: 250,
							'modal' 		: false,
						}
					);
					return false;	
	        	}
	        	return true;
			},
			
			
			
			
			
			
			onTagAdded: function(event, tag) {
				if ($(document).data("disarm_on_tagadded")) {
			        var tag = tag.text().substring(0, tag.text().length-1);
			        var tag_id = fnGetTagId(tag,data.all_tags);
					$.ajax({
						url:sprintf("/api/document/%s/tag/%s",document_id,tag_id),
						type:"POST",
						dataType:"json"
					});
				}	        	
	    	},
	    	/*	    			
			onBeforeTagRemoved:function(event,tag) {
				if (tag.text().length != 0 ) {
    				var tag_name = tag.text().substring(0, tag.text().length-1);
    				if (fnGetTagId(tag_name,data.category_tags) != null) {
		    			tag.addClass("ui-state-error");
						$("#uic_tag_message").text("A tag não pode ser deletada.");			        		
						$("#uic_tag_feedback").show("fast");
						setTimeout(function() {
					    	$("#uic_tag_feedback").hide("slow");
		    				tag.removeClass("ui-state-error");
					    }, 5000);    				
	    				return false;
	    			}
	    		}  				
	    		return true;
			},
			*/
	    	onTagRemoved: function(event, tag) {
				if (tag.text().length != 0 ) {
    				var tag_name = tag.text().substring(0, tag.text().length-1);
			        var tag_id = fnGetTagId(tag_name,data.all_tags);
					$.ajax({
						url:sprintf("/api/document/%s/tag/%s",document_id,tag_id),
						type:"DELETE",
						dataType:"json"
					});
				}
			}	        		
    	});	        		
    	$.each(data.document_tags,function(){
			$uic_tags.tagit("createTag",this.label);
		});
		
		var $uic_tag_table = $("#uic_tag_table").dataTable({
			"aaData": fnListTagLabelAndValue(data.all_tags),
			"bAutoWidth": false,
		    "aoColumns": [
	            {   "fnRender": function(obj) {
					   return sprintf(
					   	 "<a id='uic_addtag_link' rel='addtag_link' href='%s' class='ui-icon ui-icon-squaresmall-plus'></a>",
					   	 obj.aData[obj.iDataColumn]
					   );
				   	},
				   	"sWidth":"1px"
	             },
	             null
	        ],				
	        "sScrollY": "200px",
	        "bPaginate": false,
			"oLanguage": {
				"sSearch": "Buscar",
				"sInfo": "_TOTAL_ tag(s) encontrada(s)",
				"sInfoFiltered": "(total _MAX_)",
			}		        
		});
		
		$("a[rel='addtag_link']").click(function(){
			$(this).addClass("ui-state-disabled");
			var tag_id = $(this).attr('href');
			$uic_tags.tagit("createTag", fnGetTagLabel(tag_id,data.all_tags));
			return false;
		});		
										
		$(document).data("disarm_on_tagadded",true);	       
	});
	
				
	
	
	
	
	
	
	
	//TODO: Refactor unir com o search.xhtml
	$("a[rel=uic_download-file_link]").click(function(){
		var key = $(this).attr('href');
		$.get(sprintf(sprintf("/api/storage/key/%s",key)),{}, function(data){					
			window.location=data.url_to_download; 
		}).error(function(){
			alert("Erro ao obter a url do arquivo");
		});					
		return false;				
	});
	
	//TODO: Refactor unir com o search.xhtml
	$("a[rel=uic_visualize-file_link]").click(function(){
		var key = $(this).attr('href');
		$.get(sprintf(sprintf("/api/storage/key/%s",key)),{}, function(data){					

			$.fancybox.open([
			    {
			        href : data.url_to_preview,
			        title : data.filename,
			    }    
			], {
				type : 'iframe',
				padding    : 0,
				autoResize : false,
				maxWidth   : 800,
				maxHeight  : 600,
				fitToView  : false,
				width	   : '70%',
				height	   : '70%',
				minWidth   : 400,
				minHeight  : 300,
			});

		}).error(function(){
			alert("Erro ao obter a url do arquivo");
		});					
		return false;				
	});		
	
	
	$("#uic_taglist_link").click(function(){
		$.fancybox.open([{
				href : '/tag/dialog',
	    	}], {
				'type' 			: 'iframe',
				'autoScale' 	: false,
				'autoDimensions': false,
				'width' 		: 400,
				'height' 		: 250,
				'modal' 		: false,
				}
		);
		return false;			
	});
	
	
			

	
				
	
	
	
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

function fnCreateOrSelectTagCallback(tag_id) {
	var document_id = $(document).data("document_id");	
	$.ajax({
		url:sprintf("/api/document/%s/tag/%s",document_id,tag_id),
		type:"POST",
		dataType:"json",
		success: function(data) {
			refresh();
		}					
	});
}


