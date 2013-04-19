from django.db import models
from django.contrib.auth.models import User
from tag.models import Tag

class Category(models.Model):
	title = models.CharField(max_length=100)
	active = models.BooleanField()
	description = models.TextField(blank=True)
	created = models.DateField(auto_now=True)
	updated = models.DateField(auto_now=True)
	user = models.ForeignKey(User)
	tags = models.ManyToManyField(Tag)
			
class Attribute(models.Model):
	TYPE_CHOICES = (
		(u'S',u'Alfanumerico'),
		(u'N',u'Numerico'),		
		(u'D',u'Data'),		
	)
	name = models.CharField(max_length=30)
	type = models.CharField(max_length=2, choices=TYPE_CHOICES)
	required = models.BooleanField()
	category = models.ForeignKey(Category)	
	active = models.BooleanField(default=True, editable=False)
	order = models.PositiveSmallIntegerField(default=0, null=False)
	
	def inactivate(self):
		self.active = False
		self.save()
