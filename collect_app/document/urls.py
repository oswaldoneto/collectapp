from django.conf.urls.defaults import *
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from document.views import *
from document.api import DocTagView, DocTagListView, DocAttachView, DocDeattachView, DocNewView
from django.views.decorators.csrf import csrf_exempt
from document.s3 import FormFieldsView
from document.forms import DocumentClassifyForm
from django.contrib.auth.decorators import login_required
    
urlpatterns = patterns('',
                       
    #Class Based Generic Views    
    (r'^document/new$', login_required(TemplateView.as_view(
        template_name="app/document/document_new.xhtml"
    ))),                             
    (r'^document/new/classify$',login_required(FormView.as_view(
        template_name="app/document/document_classify_form.xhtml",
        form_class = DocumentClassifyForm        
    ))), 
    (r'^document/new/classify/category/(?P<category>\d+)$',login_required(ClassifyDocView.as_view())),
    (r'^document/(?P<document>\d+)/preview', login_required(PreviewDocView.as_view())),        
    (r'^document/(?P<document>\d+)/classify$',login_required(ClassifyDocView.as_view())),
    (r'^document/(?P<document>\d+)/classify/delete$',login_required(ClassifyDocDeleteView.as_view())),
    (r'^document/(?P<document>\d+)/classify/attribute/(?P<attribute>\d+)/add$',login_required(ClassifyDocAttributeCreateView.as_view())),
    (r'^document/(?P<document>\d+)/classify/category/(?P<category>\d+)$',login_required(ClassifyDocView.as_view())),
    (r'^document/(?P<document>\d+)/delete', login_required(DocumentDeleteView.as_view())),        
    
    #JSON API
    (r'^api/document/(?P<document>\d+)/tag/(?P<tag>\d+)$', csrf_exempt(DocTagView.as_view())),
    (r'^api/document/(?P<document>\d+)/tag$', csrf_exempt(DocTagListView.as_view())),
    (r'^api/document/(?P<document>\d+)/s3$', csrf_exempt(FormFieldsView.as_view())),
    (r'^api/document/(?P<document>\d+)/attach$', csrf_exempt(DocAttachView.as_view())),
    (r'^api/document/(?P<document>\d+)/deattach', csrf_exempt(DocDeattachView.as_view())),
    (r'^api/document/new$',csrf_exempt(DocNewView.as_view())),
        
    #TODO: REFACTOR migrate to class based generic view
    #Function Views
    (r'^document/(?P<id>\d+)/security$','document.views.security'),    
    (r'^document/(?P<document>\d+)/upload$','document.views.file_upload'),
)
