from django.conf.urls.defaults import *
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView
from document.forms import DocumentClassifyForm
from document.s3 import FormFieldsView
from document.api import DocTagView, DocTagListView, DocAttachView,\
    DocDeattachView, DocNewView, DocUserPermissionView, DocGroupPermissionView,\
    DocPublicPermissionView, DocUserPermissionsView, DocGroupPermissionsView,\
    DocPublicPermissionsView, DocNewAttachView, DocDetachView
from document.views import ClassifyDocView, PreviewDocView,\
    ClassifyDocDeleteView, ClassifyDocAttributeCreateView, DocumentDeleteView,\
    PermissionDocView
    
urlpatterns = patterns('',
                       
    #Class Based Generic Views    
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
    (r'^document/(?P<document>\d+)/permission', login_required(PermissionDocView.as_view())),        
    
    #JSON API
    (r'^api/document/(?P<document>\d+)/tag/(?P<tag>\d+)$', csrf_exempt(DocTagView.as_view())),
    (r'^api/document/(?P<document>\d+)/tag$', csrf_exempt(DocTagListView.as_view())),
    (r'^api/document/(?P<document>\d+)/permission/(?P<permission>\w+)/user/(?P<user>\d+)$', csrf_exempt(DocUserPermissionView.as_view())),
    (r'^api/document/(?P<document>\d+)/permission/(?P<permission>\w+)/group/(?P<group>\d+)$', csrf_exempt(DocGroupPermissionView.as_view())),
    (r'^api/document/(?P<document>\d+)/permission/(?P<permission>\w+)/public$', csrf_exempt(DocPublicPermissionView.as_view())),
    (r'^api/document/(?P<document>\d+)/permissions/user$', DocUserPermissionsView.as_view()),
    (r'^api/document/(?P<document>\d+)/permissions/group$', DocGroupPermissionsView.as_view()),
    (r'^api/document/(?P<document>\d+)/permissions/public$', DocPublicPermissionsView.as_view()),

    # TODO: Deprecated resources remove all references to this service before milestone v0.8.21
    #(r'^api/document/(?P<document>\d+)/s3$', csrf_exempt(FormFieldsView.as_view())),
    #(r'^api/document/(?P<document>\d+)/attach$', csrf_exempt(DocAttachView.as_view())),
    #(r'^api/document/(?P<document>\d+)/deattach', csrf_exempt(DocDeattachView.as_view())),
    #(r'^api/document/new$',csrf_exempt(DocNewView.as_view())),
    
    (r'^api/document/new/attach/key/(?P<key>\w+)$', csrf_exempt(DocNewAttachView.as_view())),
    (r'^api/document/(?P<document>\d+)/attach/key/(?P<key>\w+)$', csrf_exempt(DocAttachView.as_view())),
    (r'^api/document/(?P<document>\d+)/detach/key/(?P<key>\w+)$', csrf_exempt(DocDetachView.as_view())),
    
    
    
    
    
    
    
    
    
    
    
            
    #TODO: REFACTOR migrate to class based generic view
    #Function Views
    (r'^document/(?P<document>\d+)/upload$','document.views.file_upload'),
)
