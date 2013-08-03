from security.views import JSONResponseMixin
from django.views.generic.base import View
from django.contrib.auth.models import User, Group, Permission
from document.models import Document, DocumentAttachment,\
    DocumentPublicPermission, DocumentAttach
from django.http import HttpResponseBadRequest
from guardian.shortcuts import get_perms, get_groups_with_perms, assign,\
    remove_perm, get_users_with_perms
from tag.models import Tag
from django.shortcuts import get_object_or_404
import json
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from collect_app import settings
from document.guardianutil import clear_permission
from django.utils.decorators import method_decorator
from guardian.decorators import permission_required_or_403
from ext.views.decorator.docperm import document_permission_or_403
from storage.models import FileStorage

class DocTagView(JSONResponseMixin, View):
    def post(self,request,document,tag):
        doc = Document.objects.get(id=document)
        tag = Tag.objects.get(id=tag)
        doc.tags.add(tag)
        doc.last_update_user = request.user
        doc.save()  
        return self.render_to_response(None)
    def delete(self,request,document,tag):
        doc = Document.objects.get(id=document)
        tag = Tag.objects.get(id=tag)
        doc.tags.remove(tag)
        doc.last_update_user = request.user
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
    
#TODO: DEPRECATED
class DocNewView(JSONResponseMixin, View):
    def post(self,request):
        doc = Document(owner=self.request.user,last_update_user=self.request.user)
        doc.save()
        return self.render_to_response({"document_id":doc.id})

class DocNewAttachView(JSONResponseMixin, View):
    def post(self,request,key):
        #create document
        doc = Document(owner=self.request.user,last_update_user=self.request.user)
        doc.save()
        #create document attachment
        fs = get_object_or_404(FileStorage,key=key)
        attach = DocumentAttach(document=doc,file=fs)
        attach.save()
        return self.render_to_response({"document_id":doc.id,"filestorage_id":attach.id})
        
#TODO: DEPRECATED                                    
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
        doc.last_update_user = request.user        
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
            doc.last_update_user = request.user
            doc.save()  
        return self.render_to_response(None)
    



class DocUserPermissionsView(JSONResponseMixin, View):
    def get(self,request,document):
        doc = Document.objects.get(id=document)
        user_perms = get_users_with_perms(doc,attach_perms=True,with_group_users=False)
        return self.render_to_response(self.__parseUserPermissions(user_perms))
    def __parseUserPermissions(self,user_permissions):
        return  [ dict([('user_id',perms.id),('username',perms.username),('permission',user_permissions[perms])]) for perms in user_permissions ]    
    @method_decorator(document_permission_or_403(('read_document','change_document','delete_document'),'document'))    
    def dispatch(self, *args, **kwargs):
        return super(DocUserPermissionsView, self).dispatch(*args, **kwargs)
        
class DocGroupPermissionsView(JSONResponseMixin, View):
    def get(self, request,document):
        doc = Document.objects.get(id=document)
        group_perm = get_groups_with_perms(doc,attach_perms=True)
        return self.render_to_response(self.__parseGroupPermissions(group_perm))
    def __parseGroupPermissions(self,group_permissions):
        permissions = []
        for perms in group_permissions:
            permission = []
            permission.append(('group_id',perms.id))
            permission.append(('group_name',perms.name))
            permission.append(('permission',group_permissions[perms]))
            permissions.append(dict(permission))
        return permissions
    @method_decorator(document_permission_or_403(('read_document','change_document','delete_document'),'document'))            
    def dispatch(self, *args, **kwargs):
        return super(DocGroupPermissionsView, self).dispatch(*args, **kwargs)
    
class DocUserPermissionView(JSONResponseMixin, View):    
    def post(self,request,document,permission,user):
        user = User.objects.get(id=user)
        doc = Document.objects.get(id=document)
        assign(permission,user,doc)
        doc.last_update_user = request.user
        doc.save()          
        return self.render_to_response(get_perms(user,doc))
    def delete(self,request,document,permission,user):
        usr = User.objects.get(id=user)
        doc = Document.objects.get(id=document)
        remove_perm(permission,usr,doc)
        doc.last_update_user = request.user
        doc.save()  
        return self.render_to_response(get_perms(usr,doc))
    @method_decorator(document_permission_or_403(('change_document',),'document'))    
    def dispatch(self, *args, **kwargs):
        return super(DocUserPermissionView, self).dispatch(*args, **kwargs)
    
class DocGroupPermissionView(JSONResponseMixin, View):    
    def post(self,request,document,permission,group):
        grp = Group.objects.get(id=group)
        doc = Document.objects.get(id=document)
        assign(permission,grp,doc)
        doc.last_update_user = request.user
        doc.save()  
        return self.render_to_response(get_perms(grp,doc))
    def delete(self,request,document,permission,group):
        grp = Group.objects.get(id=group)
        doc = Document.objects.get(id=document)
        remove_perm(permission,grp,doc)
        doc.last_update_user = request.user
        doc.save()  
        return self.render_to_response(get_perms(grp,doc))
    @method_decorator(document_permission_or_403(('change_document',),'document'))        
    def dispatch(self, *args, **kwargs):
        return super(DocGroupPermissionView, self).dispatch(*args, **kwargs)
    
class DocPublicPermissionsView(JSONResponseMixin, View):
    def get(self,request,document):
        doc = Document.objects.get(id=document)
        pp_list = DocumentPublicPermission.objects.filter(document=doc)
        return self.render_to_response({"permission":[(pp.permission.codename) for pp in pp_list]})
    
    @method_decorator(document_permission_or_403(('read_document',),'document'))    
    def dispatch(self, *args, **kwargs):
        return super(DocPublicPermissionsView, self).dispatch(*args, **kwargs)

class DocPublicPermissionView(JSONResponseMixin, View):    
    def post(self,request,document,permission):
        doc = Document.objects.get(id=document)
        p = Permission.objects.filter(codename=permission)
        pp = DocumentPublicPermission(document=doc,permission=p[0])
        pp.save()
        doc.last_update_user = request.user
        doc.save()   
        return self.render_to_response(None)
    def delete(self,request,document,permission):
        doc = Document.objects.get(id=document)
        p = Permission.objects.filter(codename=permission)
        pp = DocumentPublicPermission.objects.filter(document=doc,permission=p[0])
        pp.delete()
        doc.last_update_user = request.user
        doc.save()  
        return self.render_to_response(None)
    @method_decorator(document_permission_or_403(('change_document',),'document'))    
    def dispatch(self, *args, **kwargs):
        return super(DocPublicPermissionView, self).dispatch(*args, **kwargs)
    


    
        
    
    