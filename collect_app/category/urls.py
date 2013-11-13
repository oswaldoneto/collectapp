from django.conf.urls.defaults import *
from tag.views import TagCreateView, TagEditView, TagDeleteView
from category import views
from category.api import CategoryTagListView, CategoryTagView,\
    CategoryAttributeReOrderView
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.list import ListView
from category.models import Attribute
from category.views import AttributeOrderView

urlpatterns = patterns('',
    (r'^category/list$',views.list),
    (r'^category/add$','category.views.add'),
    (r'^category/search$',views.search),
    (r'^category/(?P<category>\d+)/edit$',views.edit),
    (r'^category/(?P<category>\d+)/delete$',views.delete),
    (r'^category/(?P<category>\d+)/attribute/order$',AttributeOrderView.as_view()),
    (r'^category/(?P<category>\d+)/attribute/list$',views.list_attribute),
    (r'^category/(?P<category>\d+)/attribute/add$',views.add_attribute),
    (r'^category/(?P<category>\d+)/attribute/(?P<attribute>\d+)/edit$',views.edit_attribute),
    (r'^category/(?P<category>\d+)/attribute/(?P<attribute>\d+)/delete$',views.delete_attribute),
    (r'^category/(?P<category>\d+)/attribute/(?P<attribute>\d+)/inactive$',views.inactivate_attribute),
    (r'^category/(?P<category>\d+)/tag/list$',views.list_tag),
    (r'^category/(?P<category>\d+)/tag/add$',views.add_tag),
    (r'^category/(?P<category>\d+)/tag/delete$',views.delete_tag),
    (r'^category/search.json$',views.json_search),

    #JSON API
    (r'^api/category/(?P<category>\d+)/tag$',csrf_exempt(CategoryTagListView.as_view())),
    (r'^api/category/(?P<category>\d+)/tag/(?P<tag>\d+)$',csrf_exempt(CategoryTagView.as_view())),
    (r'^api/category/(?P<category>\d+)/attribute/reorder$',csrf_exempt(CategoryAttributeReOrderView.as_view())),

)