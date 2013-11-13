from django.views.generic.edit import CreateView, UpdateView, DeleteView
from tag.forms import TagForm
from tag.models import Tag
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from document.search_indexes import DocumentIndex
from django.views.generic.base import TemplateView

class TagCreateView(CreateView):
    form_class = TagForm
    success_url = "/tag/list"
    template_name = "app/tag/tag_form.xhtml"
    def form_valid(self, form):
        self.object = form.save()
        return super(TagCreateView,self).form_valid(form)
    def get_context_data(self, **kwargs):
        context = super(TagCreateView,self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context
    @method_decorator(login_required)
    @method_decorator(permission_required("tag.add_tag"))
    def dispatch(self, request, *args, **kwargs):
        return CreateView.dispatch(self, request, *args, **kwargs)

class TagEditView(UpdateView):
    model = Tag
    form_class = TagForm
    success_url = "/tag/list"
    template_name = "app/tag/tag_form.xhtml"
    def get_object(self,queryset=None):
        obj = Tag.objects.get(id=self.kwargs["tag"])
        return obj
    def get_context_data(self, **kwargs):
        context = super(TagEditView,self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context

    def form_valid(self, form):
        response = super(TagEditView,self).form_valid(form)
        #TODO: Refactor #124 and #125
        DocumentIndex().update()
        return response
    @method_decorator(login_required)
    @method_decorator(permission_required("tag.change_tag"))
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)

class TagDeleteView(DeleteView):
    success_url = "/tag/list"
    def get_object(self, queryset=None):
        obj = Tag.objects.get(id=self.kwargs["tag"])
        return obj
    @method_decorator(login_required)
    @method_decorator(permission_required("tag.delete_tag"))
    def dispatch(self, request, *args, **kwargs):
        return DeleteView.dispatch(self, request, *args, **kwargs)

class TagDialogView(TemplateView):
    template_name = "app/tag/tag.xhtml"
    def get(self, request, *args, **kwargs):
        return super(TagDialogView,self).get(request,*args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super(TagDialogView,self).get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        return context







