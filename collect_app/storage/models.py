import base64
import uuid
from django.db import models
from django.dispatch.dispatcher import receiver
from django.db.models.signals import pre_save
from django.db.models.fields import CharField
from storage.fields import UUIDField

class FileStorage(models.Model):   
    key = UUIDField(auto=True,unique=True)
    filename = models.CharField(max_length=255,null=True)
    filesize = models.IntegerField(null=True)
    filetype = models.CharField(max_length=40,null=True)
    reserved = models.BooleanField()
    storaged = models.BooleanField()
    associated = models.BooleanField()
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True, auto_now_add=True, editable=False)
    



