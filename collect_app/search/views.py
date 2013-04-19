from django.shortcuts import render_to_response
from django.template.context import RequestContext
from document.models import Document
from search.forms import TextSearchForm
from haystack.views import SearchView
from collect_app import settings

class TextSearchView(SearchView):
    def extra_context(self):
        #TODO: Refactor 72 eliminar o url_download
        return {
            'count':Document.objects.count(),
            'url_download':"https://%s/%s/document" % (settings.config.get_s3_host(),settings.config.get_s3_bucket())
        }
    
    


















