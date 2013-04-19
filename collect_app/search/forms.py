from haystack.forms import ModelSearchForm
from haystack.inputs import AutoQuery

class TextSearchForm(ModelSearchForm):
    def search(self):
        if not self.is_valid():
            return self.no_query_found()
        if not self.cleaned_data.get('q'):
            return self.no_query_found()
        query = self.cleaned_data['q']
        kwords = iter(set(query.split()))
        sqs = self.searchqueryset
        for kword in kwords:
            sqs = sqs.filter_or(content__contains=kword)
        if self.load_all:
            sqs = sqs.load_all()
        return sqs