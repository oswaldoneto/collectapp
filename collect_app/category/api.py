from django.contrib.auth.models import User, Group
from django.http import HttpResponseBadRequest
from django.views.generic.base import View
from document.guardianutil import modify_permission, get_user_permission, \
    clear_permission
from document.models import Document
from guardian.shortcuts import get_perms, get_groups_with_perms
from security.views import JSONResponseMixin
from tag.models import Tag
from category.models import Category, Attribute
from django.shortcuts import get_object_or_404

class CategoryTagListView(JSONResponseMixin, View):
    def get(self,request,category):        
        cat = get_object_or_404(Category,pk=category)
        return self.render_to_response({
            "category_tags":self.dict_tag(cat.tags.all()),
            "all_tags":self.dict_tag(Tag.objects.all())
        })
    def dict_tag(self,tag_objects):  
        return [({"value":tag.id,"label":tag.name}) for tag in tag_objects]        
        
class CategoryTagView(JSONResponseMixin, View):
    def post(self,request,category,tag):
        cat = Category.objects.get(id=category)
        tag = Tag.objects.get(id=tag)
        cat.tags.add(tag)
        return self.render_to_response(None)
    def delete(self,request,category,tag):
        cat = Category.objects.get(id=category)
        tag = Tag.objects.get(id=tag)
        cat.tags.remove(tag)
        return self.render_to_response(None)
    
class CategoryAttributeReOrderView(JSONResponseMixin, View):
    def post(self,request,category):
        ordered_ids = request.POST.getlist('id')
        for k, v in enumerate(ordered_ids):
            att = Attribute.objects.get(id=v)
            att.order = k
            att.save() 
        return self.render_to_response(None)
        
    
        
    


        
            

