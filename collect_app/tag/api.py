from security.views import JSONResponseMixin
from django.views.generic.base import View
from tag.models import Tag

class TagListView(JSONResponseMixin, View):
    def get(self,request):
        return self.render_to_response({
            "all_tags":self.dict_tag(Tag.objects.all())
        })
    def dict_tag(self,tag_objects):  
        return [({"value":tag.id,"label":tag.name}) for tag in tag_objects]        

    


        
            

