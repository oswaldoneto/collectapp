from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.contrib.auth.models import Group, User

from security import views
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import password_change, password_change_done
from django.views.generic.base import View, TemplateView
from security.views import GroupCreateView, GroupDeleteView, GroupEditView,\
    UserCreateView, UserEditView, UserDeleteView, UserChangePasswordView

urlpatterns = patterns('',
    (r'^security/group/dialog$',ListView.as_view(
        model=Group,
        template_name="app/security/group_dialog.xhtml"
    )),
    (r'^security/group/list$', login_required(ListView.as_view(
        model=Group,
        template_name="app/security/group_list.xhtml"
    ))),
    (r'^security/group/add$', GroupCreateView.as_view()),
    (r'^security/group/(?P<group>\d+)/delete$', GroupDeleteView.as_view()),
    (r'^security/group/(?P<group>\d+)/edit$', GroupEditView.as_view()),
    
    (r'^security/user/dialog$',ListView.as_view(
        model=User,
        queryset=User.objects.exclude(username="AnonymousUser"),
        template_name="app/security/user_dialog.xhtml"
    )),
    (r'^security/user/list$', ListView.as_view(
        model=User,
        queryset=User.objects.exclude(username="AnonymousUser"),
        template_name="app/security/user_list.xhtml"
    )),
    (r'^security/user/add$', UserCreateView.as_view()),
    (r'^security/user/(?P<user>\d+)/edit$', UserEditView.as_view()),
    (r'^security/user/(?P<user>\d+)/delete$', UserDeleteView.as_view()),

    (r'^security/user/password/change$', UserChangePasswordView.as_view()),
    (r'^security/user/password/change/done$', TemplateView.as_view(
         template_name="app/security/change_password_done.xhtml"
    )),


    #TODO: migrate to class based generic views
    (r'^security/permission/add$', views.add_permission),
    (r'^security/permission/delete$', views.remove_permission),
    (r'^security/permissions$', views.get_permissions),
    
    #JSON API
    #(r'^security/permission/user/(?P<user_id>\d+)/document/(?P<doc_id>\d+)$', login_required(csrf_exempt(DocUserPermissionView.as_view()))),
    #(r'^security/permissions/users/document/(?P<doc_id>\d+)$', DocUserPermissionsView.as_view()),
    #(r'^security/permission/group/(?P<group_id>\d+)/document/(?P<doc_id>\d+)$', csrf_exempt(DocGroupPermissionView.as_view())),
    #(r'^security/permissions/groups/document/(?P<doc_id>\d+)$', csrf_exempt(DocGroupPermissionsView.as_view()))),
)