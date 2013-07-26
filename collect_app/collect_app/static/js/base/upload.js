
//Teste Git Branch - Pull Request solicitado inclusao

$(document).ready(function(){	
	
    var document_id = $(document).data("document_id");		
    
	//TODO: Refactor 72
    $("#uic_new_upload_form").fileupload({
		forceIframeTransport: true,
		autoUpload:true,
		add:function(e,data) {
			pleaseWait();						
			$.post("/api/document/new",{},function(doc_info){
				doc_id = doc_info.document_id;
				$.get( sprintf("/api/document/%s/s3",doc_id),{},function(fields){
					$("#uic_new_upload_form input:hidden[name=AWSAccessKeyId]").val(fields.access_key_id);
					$("#uic_new_upload_form input:hidden[name=policy]").val(fields.policy);
					$("#uic_new_upload_form input:hidden[name=signature]").val(fields.signature);		
					$("#uic_new_upload_form input:hidden[name=acl]").val(fields.acl);		
					$("#uic_new_upload_form input:hidden[name=key]").val(fields.key);		
					$("#uic_new_upload_form input:hidden[name=success_action_status]").val("200");
					$("#uic_new_upload_form ").attr("action",fields.bucket_url);  					
					data.submit();
				});						
			});
		},
		done:function(e,data) {
			$.post(sprintf("/api/document/%s/attach",doc_id),{
				name:data.files[0].name,
				type:data.files[0].type,
				size:data.files[0].size
			},function(data){
				redirect(sprintf("/document/%s/preview",doc_id));						
			}).error(function(){
				alert('erro'); 
			});		
		},
    });	
    
    //TODO: Refactor 72
	$('#uic_upload_form').fileupload({
		forceIframeTransport:true,
		autoUpload:true,
		add: function(e,data) {	
			pleaseWait();					
			var document_id = $(document).data("document_id");				
			$.get(sprintf("/api/document/%s/s3",document_id),{},function(fields){
				$("#uic_upload_form input:hidden[name=AWSAccessKeyId]").val(fields.access_key_id);
				$("#uic_upload_form input:hidden[name=policy]").val(fields.policy);
				$("#uic_upload_form input:hidden[name=signature]").val(fields.signature);		
				$("#uic_upload_form input:hidden[name=acl]").val(fields.acl);		
				$("#uic_upload_form input:hidden[name=key]").val(fields.key);		
				$("#uic_upload_form input:hidden[name=success_action_status]").val("200");
				$("#uic_upload_form").attr("action",fields.bucket_url);  
				data.submit();	
			});		        
		},
		done:function(e,data) {
			$.post(sprintf("/api/document/%s/attach",document_id),{
				name:data.files[0].name,
				type:data.files[0].type,
				size:data.files[0].size
			},function(data){
				redirect(sprintf("/document/%s/preview",document_id));						
			}).error(function(){
				alert('erro'); 
			});	
		},			
	});
});