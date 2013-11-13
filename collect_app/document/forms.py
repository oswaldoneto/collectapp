from django import forms
from category.models import Category, Attribute
from _pyio import __metaclass__
from django.forms.forms import BaseForm, get_declared_fields
from django.utils.datastructures import SortedDict
from document.widgets import DateWidget
from document import models
from document.models import Document
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.db import transaction

class DocumentForm(forms.Form):
    pass

class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s" % obj.title    

class DocumentClassifyMetaclass(type):
    
    CATEGORY_FIELD_NAME = "category"
    DOCUMENT_FIELD_NAME = "document"
    
    FIELD_NAME_PREFIX = "field"
    
    def __call__(self, *args, **kwargs):        
        form_fields = [(self.CATEGORY_FIELD_NAME,CategoryModelChoiceField(queryset=Category.objects.all().order_by("title"),empty_label=""))]
        initial = kwargs['initial']
        if self.DOCUMENT_FIELD_NAME in initial and self.CATEGORY_FIELD_NAME in initial:
            doc = get_object_or_404(Document,pk=initial[self.DOCUMENT_FIELD_NAME])
            if doc.category:
                form_fields.extend(self.__form_fields_from_document(initial[self.DOCUMENT_FIELD_NAME]))                    
            else:
                form_fields.extend(self.__form_fields_from_category(initial[self.CATEGORY_FIELD_NAME]))
        elif self.CATEGORY_FIELD_NAME in initial:            
            form_fields.extend(self.__form_fields_from_category(initial[self.CATEGORY_FIELD_NAME]))
        self.base_fields = SortedDict(form_fields)
        return  super(DocumentClassifyMetaclass,self).__call__(*args, **kwargs)
    def __form_fields_from_category(self,category_id):
        cat = Category.objects.get(id=category_id)
        attrs = Attribute.objects.filter(category=cat,active=True).order_by('order')
        form_fields = []
        for attr in attrs:
            form_fields.append(self.__field(attr))
        return form_fields
    def __form_fields_from_document(self,document_id):        
        doc = models.Document.objects.get(id=document_id)
        doc_attrs = models.DocumentAttribute.objects.filter(document=doc)
        form_fields = []
        for doc_attr in doc_attrs:
            form_fields.append(self.__field(doc_attr.attribute))
        return form_fields
    def __field(self,attr):
        if attr.type == 'N':
            form_field = forms.IntegerField(label=attr.name,required=attr.required,min_value=1, max_value=999999999999999999)
        elif attr.type == 'S':
            form_field = forms.CharField(label=attr.name,required=attr.required) 
        elif attr.type == 'D':
            form_field = forms.DateField(label=attr.name,required=attr.required,widget=DateWidget(format='%d/%m/%Y'),input_formats=['%d/%m/%Y'])
        else:
            raise TypeError()            
        return (DocumentClassifyMetaclass.field_name(attr),form_field)
    @staticmethod
    def field_name(attr):
        return "%s%s" % (DocumentClassifyMetaclass.FIELD_NAME_PREFIX,attr.id)

class DocumentClassifyForm(BaseForm):
    __metaclass__ = DocumentClassifyMetaclass    
    @method_decorator(transaction.commit_on_success)
    def save(self,request):
        doc = None
        if DocumentClassifyMetaclass.DOCUMENT_FIELD_NAME in self.initial:
            doc = models.Document.objects.get(id=self.initial[DocumentClassifyMetaclass.DOCUMENT_FIELD_NAME])
        cat = None
        doc_attrs = []                
        for field_name, field_value in self.cleaned_data.iteritems():
            if field_name == DocumentClassifyMetaclass.CATEGORY_FIELD_NAME:
                cat = field_value
            else:
                attr_id = field_name[len(DocumentClassifyMetaclass.FIELD_NAME_PREFIX):]
                attr = Attribute.objects.get(id=attr_id)
                if doc and doc.category:
                    doc_attr = models.DocumentAttribute.objects.filter(document=doc,attribute=attr)[0]
                else:
                    doc_attr =  models.DocumentAttribute(attribute=attr)
                doc_attr.set_native_value(field_value)
                doc_attrs.append(doc_attr)
        if not doc:
            doc = models.Document(category=cat,owner=request.user,last_update_user=request.user)
        if doc and not doc.category:
            doc.category = cat
        doc.save()                
        for doc_attr in doc_attrs:
            doc_attr.document = doc
            doc_attr.save()
        doc.last_update_user = request.user
        doc.save()
        return doc