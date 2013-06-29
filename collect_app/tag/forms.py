from django import forms
from tag.models import Tag

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
    def clean_name(self):
        data = self.cleaned_data['name']
        if " " in data:
            raise forms.ValidationError("Nao e permitido espaco em branco no nome da tag.")
        return data