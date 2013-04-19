from security.views import JSONResponseMixin
from django.views.generic.base import View
from django.contrib.auth.models import User, Group
from document.models import Document
from django.http import HttpResponseBadRequest
from document.guardianutil import modify_permission, get_user_permission, clear_permission
from guardian.shortcuts import get_perms, get_groups_with_perms

class DocUserPermissionView(JSONResponseMixin, View):
    def get(self, request,user_id,doc_id):
        user = User.objects.get(id=user_id)
        doc = Document.objects.get(id=doc_id)
        group_perm = get_perms(user,doc)
        return self.render_to_response(self.__parseUserPermission(user,group_perm))
    def post(self,request,user_id,doc_id):
        user = User.objects.get(id=user_id)
        doc = Document.objects.get(id=doc_id)
        try:
            permission = request.POST['permission']
        except KeyError:
            return HttpResponseBadRequest()
        modify_permission(user,doc,permission)
        return self.render_to_response(None)
    def delete(self,request,user_id,doc_id):
        user = User.objects.get(id=user_id)
        doc = Document.objects.get(id=doc_id)
        clear_permission(user,doc)
        return self.render_to_response(None)
    def __parseUserPermission(self,user,permission):
        return dict([('user_id',user.id),('username',user.username),('permission',permission)])
    
        
class DocUserPermissionsView(JSONResponseMixin, View):
    def get(self,request,doc_id):
        doc = Document.objects.get(id=doc_id)
        user_perms = get_user_permission(doc)
        return self.render_to_response(self.__parseUserPermissions(user_perms))
    def __parseUserPermissions(self,user_permissions):
        return  [ dict([('user_id',perms.id),('username',perms.username),('permission',user_permissions[perms])]) for perms in user_permissions ] 
    

class DocGroupPermissionView(JSONResponseMixin, View):
    def get(self, request,group_id,doc_id):
        group = Group.objects.get(id=group_id)
        doc = Document.objects.get(id=doc_id)
        group_perm = get_perms(group,doc)
        return self.render_to_response(self.__parseGroupPermission(group,group_perm))
    def delete(self,request,group_id,doc_id):
        group = Group.objects.get(id=group_id)
        doc = Document.objects.get(id=doc_id)
        clear_permission(group,doc)
        return self.render_to_response(None)
    def post(self, request,group_id,doc_id):
        group = Group.objects.get(id=group_id)
        doc = Document.objects.get(id=doc_id)
        try:
            permission = request.POST['permission']  
        except KeyError:
            return HttpResponseBadRequest()
        modify_permission(group,doc,permission)
        return self.render_to_response(None)
    def __parseGroupPermission(self,group,permission):
        return dict([('group_id',group.id),('group_name',group.name),('permission',permission)])
 
    
class DocGroupPermissionsView(JSONResponseMixin, View):
    def get(self, request,doc_id):
        doc = Document.objects.get(id=doc_id)
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
        
        
        
            

