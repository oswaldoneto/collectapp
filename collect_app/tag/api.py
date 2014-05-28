from security.views import JSONResponseMixin
from django.views.generic.base import View
from tag.models import Tag
from django.views.decorators.csrf import csrf_exempt

class TagView(JSONResponseMixin, View):
    def post(self,request):
        tag = Tag(name=request.POST['name'])
        tag.save()
        return self.render_to_response({"tag_id":tag.id})
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(TagView, self).dispatch(*args, **kwargs)