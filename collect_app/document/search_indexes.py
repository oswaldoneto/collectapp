# -*- coding: utf-8 -*-
from django.db.models import signals
from document.models import Document, DocumentAttribute
from haystack import indexes
import datetime
from tag.models import Tag
    
class DocumentIndex(indexes.SearchIndex, indexes.Indexable):        
    text = indexes.CharField(document=True,use_template=True)
    updated = indexes.DateTimeField(model_attr='updated')
    owner = indexes.CharField(model_attr='owner__username',indexed=True)
    category = indexes.CharField(model_attr='category__title',faceted=True,null=True)
    tags = indexes.MultiValueField(faceted=True)

    def get_model(self):
        return Document
    
    def prepare_tags(self,obj):
        return [(tag.name) for tag in obj.all_tags() ]
