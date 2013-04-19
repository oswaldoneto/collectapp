from django.db.models import signals
from document.models import Document, DocumentAttribute
from haystack import indexes
import datetime
    
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):        
    text = indexes.CharField(document=True,use_template=True)
    updated = indexes.DateTimeField(model_attr='updated')
    owner = indexes.CharField(model_attr='owner__username',indexed=True)
    def get_model(self):
        return Document
    #def index_queryset(self):
    #    return self.get_model().objects.filter(updated__lte=datetime.datetime.now())
