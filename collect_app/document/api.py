from security.views import JSONResponseMixin
from django.views.generic.base import View
from django.contrib.auth.models import User, Group
from document.models import Document, DocumentAttachment
from django.http import HttpResponseBadRequest
from document.guardianutil import modify_permission, get_user_permission, clear_permission
from guardian.shortcuts import get_perms, get_groups_with_perms
from tag.models import Tag
from django.shortcuts import get_object_or_404
import json
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from collect_app import settings

class DocTagView(JSONResponseMixin, View):
    def post(self,request,document,tag):
        doc = Document.objects.get(id=document)
        tag = Tag.objects.get(id=tag)
        doc.tags.add(tag)
        doc.save()
        return self.render_to_response(None)
    def delete(self,request,document,tag):
        doc = Document.objects.get(id=document)
        tag = Tag.objects.get(id=tag)
        doc.tags.remove(tag)
        doc.save()
        return self.render_to_response(None)
    
class DocTagListView(JSONResponseMixin, View):
    def get(self,request,document):
        doc = get_object_or_404(Document,pk=document)
        return self.render_to_response({
            "document_tags":self.dict_tag(doc.all_tags()),
            "category_tags":self.dict_tag(doc.category.tags.all()),
            "all_tags":self.dict_tag(Tag.objects.all())
        })
    def dict_tag(self,tag_objects):  
        return [({"value":tag.id,"label":tag.name}) for tag in tag_objects]
    
class DocNewView(JSONResponseMixin, View):
    def post(self,request):
        doc = Document(owner=self.request.user,last_update_user=self.request.user)
        doc.save()
        return self.render_to_response({"document_id":doc.id})
                                    
class DocAttachView(JSONResponseMixin, View):
    def post(self,request,document):
        doc = get_object_or_404(Document,pk=document)        
        attach = DocumentAttachment()
        attach.name = request.POST['name'] 
        attach.type = request.POST['type']
        attach.size = request.POST['size']
        attach.document = doc     
        attach.save()        
        #TODO: Refactor
        # Refresh updated field and force reindex for search engine. 
        # Maybe there is a way to handle with Event/listener pattern. Could be?   
        doc.save()
        return self.render_to_response(None)

class DocDeattachView(JSONResponseMixin, View):
    def post(self,request,document):
        doc = get_object_or_404(Document,pk=document)        
        for id in request.POST.getlist('ids'):
            doc_attach = get_object_or_404(DocumentAttachment,pk=id)
            #Deleta do S3
            conn = S3Connection()
            bucket = conn.get_bucket(settings.config.get_s3_bucket())
            k = Key(bucket)
            k.key = "document/%s/%s" % (doc.id,doc_attach.name)
            k.delete()
            #Deleta do banco de dados
            doc_attach.delete()
        return self.render_to_response(None)
    
        
          
    
        

            

