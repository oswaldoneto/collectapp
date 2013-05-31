from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
urlpatterns = patterns('',
    (r'^error$', TemplateView.as_view(
         template_name="app/error/error.xhtml"
    )),                                            
)
    