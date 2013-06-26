from haystack.forms import ModelSearchForm, HighlightedModelSearchForm
from haystack.inputs import AutoQuery
from haystack.query import SearchQuerySet
from django import forms

class TextSearchForm(HighlightedModelSearchForm):
    selected_category = forms.CharField(required=False,widget=forms.HiddenInput())
    selected_tag = forms.CharField(required=False,widget=forms.HiddenInput())    
    def __init__(self, *args, **kwargs):
        super(TextSearchForm,self).__init__(*args, **kwargs)
        self.current_searchqueryset = SearchQuerySet()
    
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        if not self.cleaned_data.get('q'):
            return self.no_query_found()
        sqs = self.searchqueryset
        #handles category facelet
        category = self.cleaned_data['selected_category']
        if len(category) > 0:
            sqs = sqs.narrow('category:%s' % category)   
        #handles tag facelet
        tag = self.cleaned_data['selected_tag']
        if len(tag) > 0:
            sqs = sqs.narrow('tags:%s' % tag)                     
        #handles query
        query = self.cleaned_data['q']        
        kwords = iter(set(query.split()))
        for kword in kwords:
            sqs = sqs.filter_or(content__startswith=kword)
        #highlight results    
        #sqs = sqs.highlight()
        #load results    
        if self.load_all:
            sqs = sqs.load_all()
        #used to extra_content    
        self.current_searchqueryset = sqs
        return sqs
    
