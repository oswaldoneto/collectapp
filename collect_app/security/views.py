import json

from django.views.generic.edit import CreateView, UpdateView, DeleteView,\
    FormView
from security.forms import GroupForm, ExtendedUserChangeForm,\
    ExtendedPasswordChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm,\
    PasswordChangeForm
from django.contrib.auth.models import User, Group, Permission
from security import bundle
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseBadRequest,\
    HttpResponseRedirect
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.decorators import method_decorator
from django import http
from django.db.models import Q
from django.contrib import messages
from document.models import Document


# TODO: REFACTOR move to common module 
class JSONResponseMixin(object):
    ''' Based on
        https://docs.djangoproject.com/en/dev/topics/class-based-views/
    '''
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))
    
    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return http.HttpResponse(content,
                                 content_type='application/json',
                                 **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.
        return json.dumps(context)

class GroupCreateView(CreateView):    
    form_class = GroupForm
    success_url = "/security/group/list"
    template_name = "app/security/group_create_form.xhtml"
    def form_valid(self, form):
        self.object = form.save()
        return super(GroupCreateView,self).form_valid(form)
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.add_group"))
    def dispatch(self, request, *args, **kwargs):
        return CreateView.dispatch(self, request, *args, **kwargs)
    
class GroupEditView(UpdateView):
    model = Group
    form_class = GroupForm
    success_url = "/security/group/list"
    template_name = "app/security/group_edit_form.xhtml"
    def get_object(self, queryset=None):
        obj = Group.objects.get(id=self.kwargs["group"])
        return obj
    @method_decorator(login_required)
    @method_decorator(permission_required("auth.change_group"))
    def dispatch(self, request, *args, **kwargs):
        return UpdateView.dispatch(self, request, *args, **kwargs)
   
class GroupDeleteView(DeleteView):
    success_url = "/security/group/list"
    def get_object(self, queryset=None):
        obj = Group.objects.get(id=self.kwargs["group"])
        return obj
    @method_decorator(login_required)    
    @method_decorator(permission_required("auth.delete_group"))    
    def dispatch(self, request, *args, **kwargs):
        return DeleteView.dispatch(self, request, *args, **kwargs)

class UserCreateView(CreateView):
    form_class = UserCreationForm
    success_url = "/security/user/%s/edit"
    template_name = "app/security/user_create_form.xhtml"
    def form_valid(self, form):
        self.object = form.save()
        return super(UserCreateView,self).form_valid(form)
    def get_success_url(self):
        return self.success_url % self.object.id

class UserEditView(UpdateView):
    model = User
    form_class = ExtendedUserChangeForm
    success_url = "/security/user/list"
    template_name = "app/security/user_edit_form.xhtml"
    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.kwargs["user"])
        return obj
    def form_valid(self, form):
        self.object = form.save(commit=False)
        return super(UserEditView,self).form_valid(form)

class UserDeleteView(DeleteView):
    success_url = "/security/user/list"
    def get_object(self, queryset=None):
        obj = User.objects.get(id=self.kwargs["user"])
        return obj
    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        if Document.objects.filter(Q(owner=user) | Q(last_update_user=user)).count() > 0:
            #TODO externalize message            #
            messages.error(request,'O usuario nao pode ser deletado, existem documentos referenciando o usuario. Utilize a opcao para desativar a conta do usuario.')
            return HttpResponseRedirect(self.get_success_url())
        return super(UserDeleteView,self).delete(self, request, *args, **kwargs)
        
class UserChangePasswordView(FormView):
    form_class = ExtendedPasswordChangeForm
    success_url = "/security/user/password/change/done"
    template_name = "app/security/change_password.xhtml"
    def get_initial(self):
        initial = super(UserChangePasswordView,self).get_initial()
        initial.update({'user':self.request.user})
        return initial
    def form_valid(self,form):
        form.save()
        return super(UserChangePasswordView,self).form_valid(form)        
    
    
    

#JSON API

#TODO: Refactoring based on class based generic views
@csrf_exempt
def get_permissions(request):
    if request.is_ajax() and request.method == "POST":
        ret = {}
        for key in bundle.PERMISSION_BUNDLE.iterkeys():
            bundlePerms = bundle.PERMISSION_BUNDLE[key]
            if len(bundlePerms) > 0:
                p = Permission.objects.get(codename=bundlePerms[0])
                if 'user' in request.POST:
                    user = User.objects.get(id=request.POST['user'])
                    ret[key] = user.has_perm("%s.%s" % (p.content_type.app_label, p.codename))                    
                elif 'group' in request.POST:
                    group = Group.objects.get(id=request.POST['group'])
                    ret[key] = p in group.permissions.all()
                else:
                    return HttpResponseBadRequest()
        return HttpResponse(json.dumps(ret),mimetype="application/json")
    else:
        return HttpResponseBadRequest()


#TODO: Refactoring based on class based generic views
@csrf_exempt
def add_permission(request):
    return validade_request_permission(request, True)
    
    
#TODO: Refactoring based on class based generic views
@csrf_exempt
def remove_permission(request):
    return validade_request_permission(request, False)


#TODO: Refactoring based on class based generic views
def validade_request_permission(request,check):
    if request.is_ajax() and request.method == "POST" and 'bundle' in request.POST and ('user' in request.POST or 'group' in request.POST):
        bundlename = id=request.POST['bundle']
        if 'user' in request.POST:
            user = User.objects.get(id=request.POST['user'])
            manage_user_permission(user,bundlename,check)
        else:
            group = Group.objects.get(id=request.POST['group'])
            manage_group_permission(group, bundlename, check)            
        return HttpResponse()   
    else:
        return HttpResponseBadRequest()    


#TODO: Refactoring based on class based generic views
def manage_user_permission(user,bundlename,check):
    permissions = bundle.PERMISSION_BUNDLE[bundlename]
    for permission in permissions:
        if check:
            user.user_permissions.add(Permission.objects.get(codename=permission))
        else:
            user.user_permissions.remove(Permission.objects.get(codename=permission))


#TODO: Refactoring based on class based generic views
def manage_group_permission(group,bundlename,check):
    permissions = bundle.PERMISSION_BUNDLE[bundlename]
    for permission in permissions:
        if check:
            group.permissions.add(Permission.objects.get(codename=permission))
        else:
            group.permissions.remove(Permission.objects.get(codename=permission))
    

    
    