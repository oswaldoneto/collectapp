from django.forms import ModelForm

from category.models import Category
from category.models import Attribute
from django import forms

class CategoryForm(ModelForm):
	class Meta:
		model = Category	
		exclude = ('user','tags')	

class AttributeForm(ModelForm):
	class Meta:
		model = Attribute
		exclude = ('category','order')