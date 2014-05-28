from django.db import models
from django.contrib.auth.models import User
from tag.models import Tag
from document.models import Document
from django.contrib.contenttypes.models import ContentType
from django.db.models.signals import post_save, m2m_changed
from django.dispatch.dispatcher import receiver


class Event(models.Model):
	id = models.IntegerField(primary_key=True)
	description = models.CharField(max_length=160)
	icon = models.CharField(max_length=30)


class AuditLog(models.Model):
	content_type = models.ForeignKey(ContentType,blank=True, null=True)
	object_id = models.PositiveIntegerField(blank=True, null=True)	
	user = models.ForeignKey(User)
	event = models.ForeignKey(Event)
	logged = models.DateTimeField(auto_now_add=True)


class AuditLogDetail(models.Model):
	audit_log = models.ForeignKey(AuditLog)
	description = models.CharField(max_length=160)
