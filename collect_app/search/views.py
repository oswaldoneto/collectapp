from django.shortcuts import render_to_response
from django.template.context import RequestContext
from document.models import Document
from search.forms import TextSearchForm
from haystack.views import SearchView, FacetedSearchView
from collect_app import settings

class TextSearchView(SearchView):
    def extra_context(self):
        categories = self.form.current_searchqueryset.facet('category').facet_counts()
        tags = self.form.current_searchqueryset.facet('tags').facet_counts()
        #TODO: Refactor 72 eliminar o url_download
        return {
            'categories':categories,  
            'tags':tags,  
            'count':Document.objects.count(),
            'url_download':"https://%s/%s/document" % (settings.config.get_s3_host(),settings.config.get_s3_bucket())
        } 

    
    

















