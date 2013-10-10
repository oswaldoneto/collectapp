from django.conf.urls.defaults import *
from tag.views import TagCreateView, TagEditView, TagDeleteView, TagDialogView
from tag.api import TagView

urlpatterns = patterns('',
                                              
    (r'^tag/dialog$',TagDialogView.as_view()),
                                                    
    (r'^tag/list$',TagCreateView.as_view()),                                              
    (r'^tag/add$',TagCreateView.as_view()),   
    (r'^tag/(?P<tag>\d+)/edit$',TagEditView.as_view()),
    (r'^tag/(?P<tag>\d+)/delete',TagDeleteView.as_view()),
    #JSON API
    #(r'^api/tag$',TagListView.as_view()),                                                                                           
    (r'^api/tag$',TagView.as_view()),                                                                                           
)
    