
from haystack.views import SearchView
from collect_app import settings
from guardian.shortcuts import get_perms
from ext.shortcuts import get_public_perms
from haystack.query import SearchQuerySet

from pyelasticsearch import ElasticSearch        

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
        return {
            'categories':categories,  
            'tags':tags,
        } 
    def get_results(self):
        result =  super(TextSearchView, self).get_results()
        filtered = []
        for item in result:
            if get_perms(self.request.user,item.object) or get_public_perms(item.object):
                filtered.append(item)
        #if len(filtered) == 0:
        #    es = ElasticSearch(settings.HAYSTACK_CONNECTIONS['default']['URL'])
        #    es.health()
        return filtered

    

















