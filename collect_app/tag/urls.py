from django.conf.urls.defaults import *
from tag.views import TagCreateView, TagEditView, TagDeleteView
from tag.api import TagListView
from django.views.generic.list import ListView
from tag.models import Tag

urlpatterns = patterns('',
    (r'^tag/list$',TagCreateView.as_view()),                                              
    (r'^tag/add$',TagCreateView.as_view()),   
    (r'^tag/(?P<tag>\d+)/edit$',TagEditView.as_view()),
    (r'^tag/(?P<tag>\d+)/delete',TagDeleteView.as_view()),
    #JSON API
    (r'^api/tag$',TagListView.as_view()),                                                                                           
)
    