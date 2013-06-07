from itertools import chain

from django.db import models
from django.contrib.auth.models import User, Permission

from tag.models import Tag
from ext.db.models.query import InheritanceQuerySet
from category.models import Category, Attribute
from django.contrib import auth
from django.dispatch.dispatcher import receiver
from django.db.models.signals import post_save, post_init, pre_init
from guardian.shortcuts import assign

class Document(models.Model):
	
	class Meta:permissions = (('read_document', 'Can read document'),)

	category = models.ForeignKey(Category, null=True)
	created = models.DateField(auto_now=True)
	updated = models.DateField(auto_now=True)
	owner = models.ForeignKey(User,related_name='document_owner')
	last_update_user = models.ForeignKey(User,related_name='document_last_update_user')
	tags = models.ManyToManyField(Tag, null=True)
	
	def all_tags(self):
		if not self.tags or not self.category:
			return []
		else:
			return list(chain(self.category.tags.all(), self.tags.all()))
	
	def all_attributes(self):		
		doc_attrs = DocumentAttribute.objects.filter(document=self).order_by('attribute__order')
		for doc_attr in doc_attrs:
			doc_attr.value = InheritanceQuerySet(model=AbstractValue).select_subclasses().get(id=doc_attr.value.id)
		return doc_attrs
	
	def all_new_attributes(self):
		doc_attr_ids = [(d.attribute.id) for d in DocumentAttribute.objects.filter(document=self)]
		return Attribute.objects.filter(category=self.category).exclude(id__in=doc_attr_ids).exclude(active=False)
		
	def all_files(self):
		return DocumentAttachment.objects.filter(document=self)
	
	def remove_category(self):
		if self.category:
			for doc_attr in DocumentAttribute.objects.filter(document=self):
				abstract_value = doc_attr.value
				doc_attr.delete()
				InheritanceQuerySet(model=AbstractValue).select_subclasses().get(id=abstract_value.id).delete()
				abstract_value.delete()
			self.category = None
			self.save()
			
@receiver(post_save,sender=Document)
def assign_owner_permissions(sender,**kwargs):
	if kwargs['created'] == True:
		doc = kwargs['instance']
		owner = doc.owner
		assign("read_document",owner,doc)
		assign("change_document",owner,doc)
		assign("delete_document",owner,doc)
		
		

class DocumentPublicPermission(models.Model):
	document = models.ForeignKey(Document)
	permission = models.ForeignKey(Permission)
	
class DocumentAttachment(models.Model):
	name = models.CharField(max_length=255, editable=False)
	size = models.IntegerField(editable=False)
	type = models.CharField(max_length=255, editable=False)
	created = models.DateTimeField(auto_now_add=True, editable=False)
	updated = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
	document = models.ForeignKey(Document)

class AbstractValue(models.Model):
	pass

class CharValue(AbstractValue):
	value = models.CharField(max_length=100,null=True)

class IntegerValue(AbstractValue):
	value = models.IntegerField(null=True)
	
class DateValue(AbstractValue):
	value = models.DateField(null=True)
	
class DocumentAttribute(models.Model):
	value = models.ForeignKey(AbstractValue)
	created = models.DateField(auto_now=True)
	updated = models.DateField(auto_now=True)
	document = models.ForeignKey(Document)
	attribute = models.ForeignKey(Attribute)
	def __init__(self, *args, **kwargs):
		super(DocumentAttribute,self).__init__(*args, **kwargs)
		self.native_value = None
	def save(self, *args, **kwargs):
		if self.attribute.type == 'N':
			self.value = IntegerValue(value=self.native_value)
		elif self.attribute.type == 'S':
			self.value = CharValue(value=self.native_value)
		elif self.attribute.type == 'D':
			self.value = DateValue(value=self.native_value)
		else:
			raise TypeError()				
		self.value.save()
		self.value = self.value
		return super(DocumentAttribute, self).save(*args, **kwargs)
	
	def delete(self, using=None):
		abstract_value = self.value
		InheritanceQuerySet(model=AbstractValue).select_subclasses().get(id=abstract_value.id).delete()
		abstract_value.delete()
		super(DocumentAttribute,self).delete(using=using)
		
	def set_native_value(self, native_value):
		self.native_value = native_value	
		

		
		