from django.shortcuts import render_to_response
from django.template.context import RequestContext
from document.models import Document
from search.forms import TextSearchForm
from haystack.views import SearchView, FacetedSearchView
from collect_app import settings
from guardian.shortcuts import get_perms
from ext.shortcuts import get_public_perms
from haystack.query import SearchQuerySet

class TextSearchView(SearchView):
    def extra_context(self):
        #Facet  
        categories = None
        tags = None   
        if self.results:
            sqs = SearchQuerySet()
            for item in self.results:
                sqs = sqs.filter(id=item.pk)
                categories = sqs.facet("category").facet_counts()    
                tags = sqs.facet("tags").facet_counts()  
        #TODO: Refactor 72 eliminar o url_download
        return {
            'categories':categories,  
            'tags':tags,  
            'url_download':"https://%s/%s/document" % (settings.config.get_s3_host(),settings.config.get_s3_bucket())
        } 
    def get_results(self):
        result =  super(TextSearchView, self).get_results()
        filtered = []
        for item in result:
            if get_perms(self.request.user,item.object) or get_public_perms(item.object):
                filtered.append(item)
        return filtered
    
    

















