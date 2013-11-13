from django.views.decorators.csrf import requires_csrf_token
from django.template import (Context, RequestContext,
                             loader, TemplateDoesNotExist)
from django import http

@requires_csrf_token
def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    t = loader.get_template(template_name) # You need to create a 500.html template.
    return http.HttpResponseServerError(t.render(RequestContext(request)))