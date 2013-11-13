from security.views import JSONResponseMixin
from django.views.generic.base import View
from tag.models import Tag
from django.views.decorators.csrf import csrf_exempt

#class TagListView(JSONResponseMixin, View):
#    def get(self,request):
#        return self.render_to_response({
#            "all_tags":self.dict_tag(Tag.objects.all())
#        })
#    def dict_tag(self,tag_objects):
#        return [({"value":tag.id,"label":tag.name}) for tag in tag_objects]

class TagView(JSONResponseMixin, View):
    def post(self,request):
        tag = Tag(name=request.POST['name'])
        tag.save()
        return self.render_to_response({"tag_id":tag.id})
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(TagView, self).dispatch(*args, **kwargs)