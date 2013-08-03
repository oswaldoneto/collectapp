import base64
import uuid
import hmac
import sha
from security.views import JSONResponseMixin
from django.views.generic.base import View
from storage.models import FileStorage
from collect_app import settings
import time
import simplejson
from boto.s3.connection import S3Connection
import django
from django.http import HttpResponseNotFound

class StorageAccessURLView(JSONResponseMixin, View):
    def get(self,request,key):
        bucket_url = "http://%s/%s" % (settings.config.get_s3_host(),settings.config.get_s3_bucket())
        return self.render_to_response(None)
    


class StorageReserveKeyView(JSONResponseMixin, View):
    def get(self,request):
        return self.post(request)
    def post(self,request):    
        fs = FileStorage(reserved=True)
        fs.save()
        return self.render_to_response(self.build_response(fs.key))
    def build_response(self,key):
        return {
            "bucket_url":"http://%s/%s" % (settings.config.get_s3_host(),settings.config.get_s3_bucket()),
            "access_key_id":settings.config.get_aws_access_key_id(),
            "policy":base64.b64encode(self.get_policy()),
            "signature":base64.b64encode(hmac.new(settings.config.get_aws_secret_access_key(), base64.b64encode(self.get_policy()), sha).digest()),
            "acl":"public-read",
            "key":key,
            "success_action_status":"200",
        }  
    def get_policy(self):
        expiration_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()+100000))
        return simplejson.dumps({
            "expiration": expiration_date,
            "conditions": [
                {"bucket": settings.config.get_s3_bucket()},
                {"acl": "public-read"},
                ["starts-with","$key",""],
                ["starts-with","$x-amz-meta-filename",""],
                ["starts-with","$Content-Type",""],
                {"success_action_status": "200"},
            ]
        })
        
class StorageMetadataRefreshView(JSONResponseMixin, View):
    def get(self,request,key):
        self.post(request, key)
    def post(self,request,key):
        conn = S3Connection()
        bucket = conn.get_bucket(settings.config.get_s3_bucket())
        object = bucket.get_key(key)
        if not object:
            return HttpResponseNotFound()        
        fs = FileStorage.objects.get(key=key)
        fs.filename = object.metadata["filename"]
        fs.filesize = object.size
        fs.filetype = object.content_type
        fs.storaged = True
        fs.save()   
        return self.render_to_response(None)
        

         
