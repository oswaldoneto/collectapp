from django.conf.urls.defaults import *
from search.views import TextSearchView
from django.contrib.auth.decorators import login_required
from search.forms import TextSearchForm
from haystack.views import FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet

sqs = SearchQuerySet().all().facet('category')
    
urlpatterns = patterns('',
    (r'^search$',login_required(TextSearchView(template="app/search/search.xhtml",form_class=TextSearchForm))),
    url(r'^search-entry$', FacetedSearchView(template="app/search/search_entry.xhtml",form_class=FacetedSearchForm, searchqueryset=sqs),name='haystack_search'),
)
