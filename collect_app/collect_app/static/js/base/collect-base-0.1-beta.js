function submit() {

}

function redirect(url) {
	location = url;
}

function redirectToErrorPage() {
	location = "/error";
}

function pleaseWait() {
    $.blockUI({ 
	    message: "<p class='ui-widget'><b>Por Favor Aguarde...</b></p><i class='icon-spin icon-spinner icon-large'>",
	    css: { 
	        border: 'none', 
	        padding: '15px', 
	        backgroundColor: '#000', 
	        '-webkit-border-radius': '10px', 
	        '-moz-border-radius': '10px', 
	        opacity: .5, 
	        color: '#fff' 
	    } 
    }); 
}



