from django.db.models import signals
from document.models import Document, DocumentAttribute
from haystack import indexes
import datetime
from tag.models import Tag
    
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):        
    text = indexes.CharField(document=True,use_template=True)
    updated = indexes.DateTimeField(model_attr='updated')
    owner = indexes.CharField(model_attr='owner__username',indexed=True)
    category = indexes.CharField(model_attr='category__title',faceted=True)
    tags = indexes.MultiValueField()

    def get_model(self):
        return Document
    
    def prepare_tags(self,obj):
        print 
        return [tag.name for tag in obj.all_tags() ]
        
    #def index_queryset(self):
    #    return self.get_model().objects.filter(updated__lte=datetime.datetime.now())
