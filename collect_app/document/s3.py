
# TODO: Refactor move to ext module

import time
from django.utils import simplejson
from security.views import JSONResponseMixin
from django.views.generic.base import View
import base64
import hmac
import sha
from collect_app import settings

ACL = "public-read"

class FormFieldsView(JSONResponseMixin, View):
    #TODO: Refactor 72
    def get(self,request,document):
        return self.render_to_response({
            "bucket_url":"http://%s/%s" % (settings.config.get_s3_host(),settings.config.get_s3_bucket()),
            "access_key_id":settings.config.get_aws_access_key_id(),
            "policy":base64.b64encode(self.get_policy()),
            "signature":base64.b64encode(hmac.new(settings.config.get_aws_secret_access_key(), base64.b64encode(self.get_policy()), sha).digest()),
            "acl":ACL,
            "key":"document/%s/${filename}" % document,
        })
    def get_policy(self):
        expiration_date = time.strftime('%Y-%m-%dT%H:%M:%S.000Z', time.gmtime(time.time()+10000))
        return simplejson.dumps({
            "expiration": expiration_date,
            "conditions": [
                {"bucket": settings.config.get_s3_bucket()},
                {"acl": ACL},
                ["starts-with","$key","document/"],
                {"success_action_status": "200"},
            ]
        }) 