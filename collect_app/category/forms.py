from django.forms import ModelForm

from category.models import Category
from category.models import Attribute
from django import forms

class CategoryForm(ModelForm):
	class Meta:
		model = Category	
		exclude = ('user','tags')	
	def clean_title(self):
		data = self.cleaned_data['title']
		if Category.objects.filter(title__iexact=data).count() > 0:
			#TODO externalize message
			raise forms.ValidationError("Ja existe uma categoria com este nome.")
		return data
		

class AttributeForm(ModelForm):
	class Meta:
		model = Attribute
		exclude = ('category','order')