from django.views.generic.list import ListView, BaseListView
from category.models import Attribute, Category
from django.shortcuts import render_to_response, get_object_or_404
from django.template.context import RequestContext
from django.views.generic.edit import ProcessFormView, BaseUpdateView,\
    BaseCreateView, FormView, DeleteView, BaseDeleteView
from django.forms.formsets import formset_factory
from document.forms import DocumentForm, DocumentClassifyForm,\
    DocumentClassifyMetaclass
from django.views.generic.base import TemplateView, View, RedirectView
from django.http import Http404, HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
import json
from django import http
from django.contrib.auth.models import Group, User
from document.jsonutil import parseGroupPermission,\
    parseGroupPermissions
from django.contrib.comments import get_form
from tag.api import TagListView
from tag.models import Tag
import datetime
import base64
import hmac
import sha
import time
from django.utils import simplejson
from ext.db.models.query import InheritanceQuerySet
from document.models import *
from collect_app import settings
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403, permission_required
from guardian.shortcuts import get_perms
from ext.views.decorator.docperm import document_permission_or_403

def comes_from_search(request):
    if 'HTTP_REFERER' in request.META:             
        return True if request.META['HTTP_REFERER'].find('/search') > 0 else False            
    return False
    
class PreviewDocView(TemplateView):
    template_name = "app/document/document_preview.xhtml"
    def get_context_data(self, **kwargs):
        doc = get_object_or_404(Document,id=self.kwargs['document'])
        doc_attributes = doc.all_attributes()
                
        doc_attach = DocumentAttach.objects.filter(document=doc)
        
        doc_tags = doc.all_tags()
        #set context
        context = super(PreviewDocView,self).get_context_data(**kwargs)
        context.update({'doc':doc})
        context.update({'category':doc.category})
        context.update({'attribute_list':doc_attributes})
        context.update({'attachment_list':doc_attach})
        context.update({'tag_list':doc_tags})
        context.update({'show_back_to_search':comes_from_search(self.request)})
        #TODO: Refactor 72
        context.update({'url_download':"https://%s/%s" % (settings.config.get_s3_host(),settings.config.get_s3_bucket())})
        return context    
    @method_decorator(document_permission_or_403(('read_document','change_document','delete_document'),'document'))    
    def dispatch(self, *args, **kwargs):
        return super(PreviewDocView, self).dispatch(*args, **kwargs)
        
    
    
class ClassifyDocView(FormView):
    template_name="app/document/document_classify_form.xhtml"
    form_class = DocumentClassifyForm
    success_url = "/document/%s/classify"
    def get_initial(self):
        initial = super(ClassifyDocView,self).get_initial()
        if 'category'in self.kwargs:
            initial.update({DocumentClassifyMetaclass.CATEGORY_FIELD_NAME:self.kwargs['category']})
        if 'document'in self.kwargs:
            initial.update({DocumentClassifyMetaclass.DOCUMENT_FIELD_NAME:self.kwargs['document']})
            doc = get_object_or_404(Document,id=self.kwargs['document'])
            if doc.category:            
                initial.update({DocumentClassifyMetaclass.CATEGORY_FIELD_NAME:doc.category.id})            
                for doc_attr in DocumentAttribute.objects.filter(document=doc):
                    #TODO: Refactor - Centralizar a regra de nome do componente no MetaClass
                    field_name = DocumentClassifyMetaclass.field_name(doc_attr.attribute)    
                    field_value = InheritanceQuerySet(model=AbstractValue).select_subclasses().get(id=doc_attr.value.id)
                    initial.update({field_name:field_value.value})
        return initial
    def get_context_data(self,**kwargs):
        context = super(ClassifyDocView,self).get_context_data(**kwargs)
        context.update({'params': self.kwargs})
        context.update({'show_back_to_search':comes_from_search(self.request)})
        if 'document'in self.kwargs:
            doc = get_object_or_404(Document,id=self.kwargs['document'])
            context.update({'show_tags':True if doc.category else False})
            context.update({'new_attributes':doc.all_new_attributes()})
            context.update({'doc':doc})            
        return context
    def form_valid(self, form):
        document = form.save(self.request)
        self.success_url = self.get_success_url() % document.id
        return super(ClassifyDocView,self).form_valid(form)    
    @method_decorator(document_permission_or_403(('change_document',),'document'))
    def dispatch(self, *args, **kwargs):
        return super(ClassifyDocView, self).dispatch(*args, **kwargs)

class ClassifyDocDeleteView(BaseDeleteView):
    success_url = "/document/%s/preview"
    def get_object(self, queryset=None):
        obj = Document.objects.get(id=self.kwargs["document"])
        return obj    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object() 
        self.object.remove_category()
        self.success_url = self.get_success_url() % self.object.id        
        return HttpResponseRedirect(self.get_success_url())
    
class ClassifyDocAttributeCreateView(RedirectView):
    url = "/document/%s/classify"
    def get_redirect_url(self, **kwargs):
        return self.url % (self.kwargs["document"])        
    def post(self, request, *args, **kwargs):
        doc_id = self.kwargs["document"]
        att_id = self.kwargs["attribute"]
        doc = Document.objects.get(id=doc_id)
        att = Attribute.objects.get(id=att_id)
        DocumentAttribute(document=doc,attribute=att).save()
        return super(ClassifyDocAttributeCreateView,self).post(request,*args,**kwargs)
    
class DocumentDeleteView(DeleteView):
    success_url = "/search"
    def get_object(self, queryset=None):
        obj = Document.objects.get(id=self.kwargs["document"])
        return obj
    
class PermissionDocView(TemplateView):
    template_name = "app/document/document_permission.xhtml"
    def get_context_data(self, **kwargs):
        context = super(PermissionDocView,self).get_context_data(**kwargs)
        context.update({'users':User.objects.all()})
        context.update({'groups':Group.objects.all()})
        #context.update({'document':get_object_or_404(Document,id=self.kwargs['document'])})
        context.update({'doc':get_object_or_404(Document,id=self.kwargs['document'])})
        context.update({'show_back_to_search':comes_from_search(self.request)})
        return context
    @method_decorator(document_permission_or_403(('change_document',),'document'))
    def dispatch(self, *args, **kwargs):
        return super(PermissionDocView, self).dispatch(*args, **kwargs)
    
class AttachmentDocView(ListView):
    model = DocumentAttachment
    template_name = "app/document/document_view.xhtml"






# TODO: REFACTOR migrate to class based generic views     
def file_upload(request,document):
    doc = Document.objects.get(id=document)

    access_key_id = settings.config.get_aws_access_key_id()
    secret_access_key = settings.config.get_aws_secret_access_key()
    
    bucket_url = 'http://%s/%s' % (settings.config.get_s3_host(),settings.config.get_s3_bucket())
    print bucket_url 
    
    expiration_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()+10000))
    policy =  simplejson.dumps({
        "expiration": expiration_date,
        "conditions": [
            {"bucket": settings.config.get_s3_bucket()},
            {"acl": "public-read"},
            ["starts-with","$key","document/"],
            {"success_action_status": "200"},
        ]
    })
    encodedPolicy = base64.b64encode(policy)
    print "encodedPolicy: %s" % encodedPolicy
     
    encodedSignature = base64.b64encode(hmac.new(secret_access_key, encodedPolicy, sha).digest())
    print "encodedSignature: %s" % encodedSignature
    
    return render_to_response('app/document/document_upload.xhtml',
                              {
                                'document':doc,
                                'AWSAccessKeyId':access_key_id,
                                'encodedPolicy':encodedPolicy,
                                'encodedSignature':encodedSignature,
                                'bucketURL':bucket_url                                
                              },
                              context_instance=RequestContext(request))
    