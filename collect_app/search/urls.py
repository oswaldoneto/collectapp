from django.conf.urls.defaults import *
from search.views import TextSearchView
from django.contrib.auth.decorators import login_required
from search.forms import TextSearchForm
    
urlpatterns = patterns('',
                       
    (r'^search$',login_required(TextSearchView(template="app/search/search.xhtml",form_class=TextSearchForm))),
     
)
