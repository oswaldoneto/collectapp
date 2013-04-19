from django.contrib.auth.models import User, Group
from django.http import HttpResponseBadRequest
from django.views.generic.base import View
from document.guardianutil import modify_permission, get_user_permission, \
    clear_permission
from document.models import Document
from guardian.shortcuts import get_perms, get_groups_with_perms
from security.views import JSONResponseMixin
from tag.models import Tag
from django.shortcuts import get_object_or_404
from category.models import Category

class TagListView(JSONResponseMixin, View):
    def get(self,request):
        return self.render_to_response({
            "all_tags":self.dict_tag(Tag.objects.all())
        })
    def dict_tag(self,tag_objects):  
        return [({"value":tag.id,"label":tag.name}) for tag in tag_objects]        

    


        
            

