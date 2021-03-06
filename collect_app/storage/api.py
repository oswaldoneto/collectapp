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
import boto
from boto.s3.key import Key
import urllib
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator
from document.models import DocumentAttach
from audit import signals


class StorageAccessURLView(JSONResponseMixin, View):
    
    def get(self,request,key):
        fs = FileStorage.objects.filter(key=key)[0]
        
        file_name_encoded = urllib.quote_plus(fs.filename.encode('utf-8'))
        response_headers_visualize = {'response-content-disposition': ("filename=%s" % file_name_encoded)}
        response_headers_download = {'response-content-disposition': ("attachment;filename=%s" % file_name_encoded)}
        
        c = boto.connect_s3()
        
        url_visualize = c.generate_url(90, 'GET', key=key, bucket=settings.config.get_s3_bucket(), force_http=True,response_headers=response_headers_visualize)
        url_download = c.generate_url(90, 'GET', key=key, bucket=settings.config.get_s3_bucket(), force_http=True,response_headers=response_headers_download)
        
        attach = DocumentAttach.objects.filter(file=fs)[0]
        doc = attach.document
        
        signals.post_download_attachment.send(sender=self.__class__, file=fs, document=doc, user=request.user)
        
        return self.render_to_response({
            'filename_encoded':file_name_encoded,                            
            'filename':fs.filename,
            'url_to_preview':url_visualize,
            'url_to_download':url_download,
        })
            
    @method_decorator(never_cache)            
    def dispatch(self, *args, **kwargs):
        return super(StorageAccessURLView, self).dispatch(*args, **kwargs)
        
        
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
            "acl":"authenticated-read",
            "key":key,
            "success_action_status":"200",
        }  
        
    def get_policy(self):
        expiration_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()+100000))
        return simplejson.dumps({
            "expiration": expiration_date,
            "conditions": [
                {"bucket": settings.config.get_s3_bucket()},
                {"acl": "authenticated-read"},
                ["starts-with","$key",""],
                ["starts-with","$x-amz-meta-filename",""],
                ["starts-with","$Content-Type",""],
                {"success_action_status": "200"},
            ]
        })
        
    @method_decorator(never_cache)            
    def dispatch(self, *args, **kwargs):
        return super(StorageReserveKeyView, self).dispatch(*args, **kwargs)
        
        
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
        fs.filename = object.metadata["filename"].encode('utf-8')
        fs.filesize = object.size
        fs.filetype = object.content_type
        fs.storaged = True
        fs.save()   
        return self.render_to_response(None)
    
    @method_decorator(never_cache)            
    def dispatch(self, *args, **kwargs):
        return super(StorageMetadataRefreshView, self).dispatch(*args, **kwargs)
        

         
